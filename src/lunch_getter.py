#! /usr/bin/env python3

import os
from datetime import date, timedelta, datetime
from menu import Menu

MONDAY = 0

def main():
    # Assume we always want the next up-coming monday
    days = (MONDAY - datetime.today().weekday() + 7) % 7
    start_date =  datetime.today() + timedelta(days=days)
    end_date = start_date + timedelta(days=4)
    
    while start_date <= end_date:    
        menu = Menu(os.environ['SCHOOL_ID'], os.environ['PERSON_ID'], start_date)
        menu.pretty_print()

        start_date += timedelta(days=1)

if __name__ == "__main__":
    main()
