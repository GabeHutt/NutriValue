from bs4 import BeautifulSoup
import requests
import re
import os



url = 'https://dining.umich.edu/menus-locations/dining-halls/bursley/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

def find_course(course):
    
    

print(soup)