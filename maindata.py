from diningscrape import create_menu_dict
import sqlite3
import json

def create_main_table():
    with open('tracker.json', 'r') as tracking_file:
        tracking_data = json.load(tracking_file)
    
    counter = tracking_data['hall_to_id']
    cap = counter + 25
    
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS dining_halls (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        
        
        menu_dict = create_menu_dict
        
        
        
