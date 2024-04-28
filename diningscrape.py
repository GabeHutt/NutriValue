from bs4 import BeautifulSoup
import requests
import re
import os


dining_hall_names = ['east-quad', 'west-quad', 'bursley']
url = 'https://dining.umich.edu/menus-locations/dining-halls/bursley/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

def write_database(url):
    
    

print(soup)