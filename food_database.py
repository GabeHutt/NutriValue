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
    food_info = food_response['food_description']
    print(food_info)

def main():
    get_food('nori')

if __name__ == '__main__':
    main()

