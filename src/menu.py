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

    def to_string(self):
        menu_str = f'Menu for {self.date.strftime("%A %B %-d, %Y")}\n'
        for item_type in self.item_types:
            menu_str += self.items_by_type_to_string(item_type)
        menu_str += '\n'

        return menu_str

    def items_by_type_to_string(self, item_type):
        item_str = (f'\n---{item_type}---\n')

        if item_type not in self.menu.keys():
            item_str += f'\tNo {item_type} found\n'
        else:
            for item in self.menu[item_type]:
                item_str += f'\t{item["MenuItemDescription"]}\n'
        
        return item_str
