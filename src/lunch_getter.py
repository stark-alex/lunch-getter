#! /usr/bin/env python3

import os
import json
import boto3
from datetime import date, timedelta, datetime
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

def get_configured_emails(client):
    try:
        # Retrieve email config
        resp = client.get_secret_value(SecretId='lunch-getter-config')
        logger.info("Secret retrieved successfully.")

        # return list of emails
        secret_string = json.loads(resp["SecretString"])
        email_addrs = secret_string['email_addresses'].split(',')
        return email_addrs

    except client.exceptions.ResourceNotFoundException:
        logger.info(f"The requested secret lunch-getter-config was not found.")
        raise
    except Exception as e:
        logger.error(f"An unknown error occurred: {str(e)}.")
        raise

def send_menu(client, to_addr, subject, body):
    response = client.send_email(
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

def handler(event, context):
    logger.info(event)

    menu = retrieve_weekly_menu()

    # Render the email
    email_template = load_email_template()
    email_body = email_template.render(**menu)

    # Send out emails
    sm_client = boto3.client('secretsmanager', region_name='us-east-2')
    ses_client = boto3.client('ses', region_name='us-east-2')

    for addr in get_configured_emails(sm_client):
        logger.info(f'Sending menu to {addr}')
        send_menu(ses_client, addr, f'FLA Menu for week of {next_monday().strftime("%m/%d/%Y")}', email_body)

    return { 'menu': email_body }

def main():
    resp = handler({}, {})

    with open("test_out.html", "w") as f:
        f.write(resp['menu'])

if __name__ == "__main__":
    main()
