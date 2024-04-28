import requests
import os
import sqlite3
import json
import re

def make_main_table():
    connect = sqlite3.connect("NutriValue.db")
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS fatsecret (id INTEGER NOT NULL PRIMARY KEY, calories REAL, fat REAL, carbs REAL, protein REAL, fat_score REAL, carb_score REAL, protein_score REAL)")
    f = open('tracker.json')
 
    data = json.load(f)

    current_count = data['last_id']
    for i in range(0,25):

