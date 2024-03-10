import requests, json

class Menu:
    def __init__(self, school_id, person_id, date):
        params = {
            'SchoolId': school_id,
            'ServingDate': date.strftime("%m/%d/%Y"),
            'ServingLine': 'Main',
            'MealType': 'Lunch',
            'Grade': '03',
            'PersonId': person_id
        }
        url = 'https://webapis.schoolcafe.com/api/CalendarView/GetDailyMenuitemsByGrade'
        r = requests.get(url, params=params)

        self.date = date
        self.menu = json.loads(r.text)
        self.item_types = ["ENTREES", "VEGETABLES", "FRUITS"]


    def pretty_print(self):
        print(f'Menu for {self.date.strftime("%A %B %-d, %Y")}')
        for item_type in self.item_types:
            self.print_item_by_type(item_type)
        print('\n')

    def print_item_by_type(self, item_type):
        print(f'\n---{item_type}---')

        if item_type not in self.menu.keys():
            print (f'\tNo {item_type} found')
        else:
            for item in self.menu[item_type]:
                print(f'\t{item["MenuItemDescription"]}')