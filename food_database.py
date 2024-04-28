import requests
import os
import sqlite3
import json
import re
from fatsecret import Fatsecret

API_ID = '8ab25fc9a2ef4f6da52799c3ccda208e'

API_SECRET = '4a269d09d9a04870be65fc4d777bcfae'

fs = Fatsecret(API_ID, API_SECRET)
    
def get_food(name):
    try:
        food_response = fs.foods_search(name, 1, 1)
        food_info = str(food_response['food_description'])
        print(food_response)

        calories = re.findall(r"(\d{2})kcal", food_info)[0]
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
    connection = sqlite3.connect("NutriValueDB")
    #create table for the fatsecret API return values
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS food_nutrtition (id TEXT, calories REAL, fat REAL, carbs REAL, protein REAL)"
    )



def store_items():
    final_id = 0
    with open('tracker.json', 'r') as tracking_file:
        tracking_data = json.load(tracking_file)
    current_count = tracking_data['last_id']
    connection = sqlite3.connect("NutriValue.db")
    cursor = connection.cursor()
    for i in range(0,25):
        food_retrieve = cursor.execute("SELECT name FROM food_names WHERE id=?"(current_count + i,))
        food_name = food_retrieve.fetchone()[0]
        res = cursor.execute("SELECT name FROM food_nutrition WHERE food_name=?",(food_name,))
        if res.fetchone() is None:
            food_nutrition = get_food(food_name)
            if food_nutrition is not None:
                protein_score = (food_nutrition[4] * 9 / food_nutrition[1]) * 100
                fat_score = (food_nutrition[2] * 4 / food_nutrition[1]) * 100
                carb_score = (food_nutrition[3] * 4 / food_nutrition[1]) * 100
                true_nutrition = food_nutrition + (fat_score, carb_score, protein_score)
                cursor.execute('INSERT INTO food_nutrition (id, calories, fat, carbs, protein, fat_score , carb_score, protein_score) VALUES(?,?,?,?,?,?,?)', true_nutrition)
        final_id = current_count + i
    tracking_data['last_id'] = final_id
    with open('tracker.json', 'w') as write:
        json.dump(tracking_data, write)



if __name__ == '__main__':
    main()


