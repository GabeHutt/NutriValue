import requests
import os
import sqlite3
import json
import re
from fatsecret import Fatsecret

api_json = None

with open('API.json', 'r') as apis:
        api_json = json.load(apis)

API_ID = api_json['API_ID']

API_SECRET = api_json['API_SECRET']

fs = Fatsecret(API_ID, API_SECRET)
    
def get_food(name):
    if re.match(f"[Ss]ervice", name):
        return None
    if re.findall(f"[Gg]rilled",name):
        pattern = r"(.*?)(?:[Gg]rilled)(.*)"
        matches = re.findall(pattern, name)
        name = "".join(matches[0])
    if re.findall(f"[Ss]liced",name):
        pattern = r"(.*?)(?:[Ss]liced)(.*)"
        matches = re.findall(pattern, name)
        name = "".join(matches[0])
    try:
        food_response = fs.foods_search(name, 1, 1)
        food_info = str(food_response['food_description'])
        calories = re.findall(r"(\d*)kcal", food_info)[0]
        fat = re.findall(r'Fat: (\d*\.\d{2})g', food_info)[0]
        carbs = re.findall(r'Carbs: (\d*\.\d{2})g', food_info)[0]
        protein = re.findall(r'Protein: (\d*\.\d{2})g', food_info)[0]
        return (float(calories), float(fat), float(carbs), float(protein))
    except:
        return None

def main():
    make_database()
    store_items()
    



def make_database():
    connection = sqlite3.connect("NutriValue.db")
    #create table for the fatsecret API return values
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS food_nutrition (food_name_id INT, calories REAL, fat REAL, carbs REAL, protein REAL, fat_score REAL, carb_score REAL, protein_score REAL)"
    )
    connection.commit()



def store_items():
    final_id = 0
    with open('tracker.json', 'r') as tracking_file:
        tracking_data = json.load(tracking_file)
    current_count = tracking_data['last_id'] + 1
    connection = sqlite3.connect("NutriValue.db")
    cursor = connection.cursor()
    for i in range(0,25):
        food_retrieve = cursor.execute("SELECT name FROM food_names WHERE id=?",(current_count + i,))
        flag = food_retrieve.fetchone()
        if flag is not None:
            food_name = flag[0]
        else:
            continue
        res = cursor.execute("SELECT food_name_id FROM food_nutrition WHERE food_name_id=?",(current_count + i,))
        if res.fetchone() is None:
            food_nutrition = get_food(food_name)
            if food_nutrition is not None:
                protein_score = round((food_nutrition[3] * 4 / food_nutrition[0]) * 100, 2)
                fat_score = round((food_nutrition[1] * 9 / food_nutrition[0]) * 100 , 2)
                carb_score = round((food_nutrition[2] * 4 / food_nutrition[0]) * 100 , 2)
                true_nutrition = (current_count + i,) + food_nutrition + (fat_score, carb_score, protein_score)
                cursor.execute('INSERT INTO food_nutrition (food_name_id, calories, fat, carbs, protein, fat_score , carb_score, protein_score) VALUES(?,?,?,?,?,?,?,?)', true_nutrition)
                connection.commit()
        final_id = current_count + i
    tracking_data['last_id'] = final_id
    with open('tracker.json', 'w') as write:
        json.dump(tracking_data, write)
    
    if final_id is tracking_data['name_to_id']:
        print('No More Nutritional Information To Gather, Please Run key_tables then maindata!')

if __name__ == '__main__':
    main() 


