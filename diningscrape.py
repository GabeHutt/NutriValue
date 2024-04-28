from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3




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




def write_database(url):
    pass
    
