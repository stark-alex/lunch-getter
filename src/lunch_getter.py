#! /usr/bin/env python3

import os
import json
import boto3
from datetime import timedelta, datetime
from time import sleep
from menu import Menu
import logging
import jinja2

logger = logging.getLogger()
logger.setLevel("INFO")

MONDAY = 0

def next_monday():
    days = (MONDAY - datetime.today().weekday() + 7) % 7
    return datetime.today() + timedelta(days=days)

def retrieve_weekly_menu():
    # Find the next Monday
    start_date = next_monday()
    end_date = start_date + timedelta(days=4)
    
    # Build the menu for the week
    full_menu = {
        'date': start_date.strftime('%A %B %-d, %Y'),
        'daily_menus': []
    }
    while start_date <= end_date:
        menu = Menu(os.environ['SCHOOL_ID'], os.environ['PERSON_ID'], start_date)
        full_menu["daily_menus"].append(menu.get())
        start_date += timedelta(days=1)
    
    return full_menu

def load_email_template():
    loader = jinja2.FileSystemLoader(searchpath='./templates')
    template_env = jinja2.Environment(loader=loader)
    return template_env.get_template('email.template')

def send_menu(client, to_addr, subject, body):
    # Sleep a bit to avoid sandbox ses limitations
    sleep(2)
    try:
        client.send_email(
            Source='stark.1380@gmail.com',
            Destination={
                'ToAddresses': [to_addr]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Html': {
                        'Data': body
                    }
                }
            }
        )
    except Exception as e:
        logger.error(f"An error occurred while sending email to {to_addr}: {str(e)}.")

def handler(event, context):
    logger.info(event)

    menu = retrieve_weekly_menu()

    # Render the email
    email_template = load_email_template()
    email_body = email_template.render(**menu)

    # Send out emails
    sm_client = boto3.client('secretsmanager', region_name='us-east-2')
    ses_client = boto3.client('ses', region_name='us-east-2')

    email_addrs = os.environ["EMAILS"].split(',')
    for addr in email_addrs:
        logger.info(f'Sending menu to {addr}')
        send_menu(ses_client, addr, f'FLA Menu for week of {next_monday().strftime("%m/%d/%Y")}', email_body)

    return { 'menu': email_body }

def main():
    resp = handler({}, {})

    with open("test_out.html", "w") as f:
        f.write(resp['menu'])

if __name__ == "__main__":
    main()
