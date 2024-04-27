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
    food_response = fs.foods_search(name, 1, 1)
    food_info = str(food_response['food_description'])
    print(food_info)
    calories = re.findall(r"(\d{2})kcal", food_info)[0]
    fat = re.findall(r'Fat: (\d*\.\d{2})g', food_info)[0]
    carbs = re.findall(r'Carbs: (\d*\.\d{2})g', food_info)[0]
    protein = re.findall(r'Protein: (\d*\.\d{2})g', food_info)[0]
    return (float(calories), float(fat), float(carbs), float(protein))

def main():
    get_food('nori')

if __name__ == '__main__':
    main()

