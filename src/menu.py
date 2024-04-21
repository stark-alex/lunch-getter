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

    def get(self):
        menu = { 'day': self.date.strftime('%A') }

        if menu:
            menu['entrees'] = self.get_items_by_type("ENTREES")
            menu['veggies'] = self.get_items_by_type("VEGETABLES")
            menu['fruits'] = self.get_items_by_type("FRUITS")

        return menu

    def get_items_by_type(self, item_type):
        items = []
        if item_type not in self.menu.keys():
            items.append(f'\tNo {item_type} found\n')
        else:
            for item in self.menu[item_type]:
                items.append(f'\t{item["MenuItemDescription"]}\n')
        
        return items
