#! /usr/bin/env python3

import os
import json
import boto3
from datetime import date, timedelta, datetime
from menu import Menu
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

MONDAY = 0

def get_configured_emails():
    try:
        client = boto3.client('secretsmanager', region_name='us-east-2')
        resp = client.get_secret_value(SecretId='lunch-getter-config')
        logger.info("Secret retrieved successfully.")
        secret = json.loads(resp["SecretString"])
        return secret['email_addresses'].split(',')
    except client.exceptions.ResourceNotFoundException:
        msg = f"The requested secret lunch-getter-config was not found."
        logger.info(msg)
        return msg
    except Exception as e:
        logger.error(f"An unknown error occurred: {str(e)}.")
        raise

def send_menu(to_addr, subject, body):
    client = boto3.client('ses', region_name='us-east-2')
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
                'Text': {
                    'Data': body
                }
            }
        }
    )
    return response['MessageId']

def next_monday():
    days = (MONDAY - datetime.today().weekday() + 7) % 7
    return datetime.today() + timedelta(days=days)

def handler(event, context):
    logger.info(event)

    # Find the next Monday
    start_date =  next_monday()
    end_date = start_date + timedelta(days=4)
    
    # Build the menu for the week
    full_menu_str = ''
    while start_date <= end_date:
        menu = Menu(os.environ['SCHOOL_ID'], os.environ['PERSON_ID'], start_date)
        full_menu_str += menu.to_string()
        start_date += timedelta(days=1)

    for addr in get_configured_emails():
        logger.info(f'Sending menu to {addr}')
        send_menu(addr, f'FLA Menu for week of {next_monday().strftime("%m/%d/%Y")}', full_menu_str)

    return { 'menu': full_menu_str }

def main():
    resp = handler({}, {})
    print(resp['menu'])

if __name__ == "__main__":
    main()
