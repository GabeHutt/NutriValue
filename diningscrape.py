from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3
import json




dining_hall_names = ['east-quad', 'bursley', 'south-quad', 'markley',
                     'mosher-jordan', 'twigs-at-oxford', 'north-quad'
                     ]

def get_menu(dining_hall):
    url = f'https://dining.umich.edu/menus-locations/dining-halls/{dining_hall}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_items = soup.find(id="mdining-items")
    course_names = ['breakfast', 'brunch', 'dinner']
    courses = all_items.find_all('ul', class_='courses_wrapper')
    dining_menu = {}
    course_num = 0
    for course in courses:
        course_name = course_names[course_num]
        course_num += 1
        items = course.find_all('ul', class_='items' )
        dining_menu[course_name] = []
        for item in items:
            food_names = item.find_all('div', class_='item-name')
            for food_name in food_names:
                name = food_name.text.rstrip()
                if re.search(r"w/", name):
                    name = re.findall(r"(.+) w/", name)[0]
                dining_menu[course_name].append(name)
    return dining_menu


def create_menu_dict():
    return {name: get_menu(name) for name in dining_hall_names}


def write_name_to_id():
    with open('tracker.json', 'r') as tracking_file:
        tracking_data = json.load(tracking_file)
    
    counter = tracking_data['name_to_id']
    cap = counter + 25
    
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS food_names (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        
        
        menu_dict = create_menu_dict
        
        record_mode = False
        new_counter = 0

        for dining_hall, meals_dict in menu_dict.items():
            for course, meals in meals_dict.items():
                for meal in meals:
                    if new_counter == counter:
                        record_mode = True
                    if record_mode and counter < cap:
                        curr.execute("INSERT INTO food_names (name) VALUES (?)", (meal,))
                        counter += 1
                    new_counter += 1

        tracking_data['name_to_id'] = counter
        with open('tracker.json', 'w') as tracking_file:
            json.dump(tracking_data, tracking_file)

        connection.commit()


    


write_name_to_id()

                
            
                
        

           
    
    
