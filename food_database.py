import requests
import os
import sqlite3
import json
import re
from fatsecret import Fatsecret

API_ID = '8ab25fc9a2ef4f6da52799c3ccda208e'

API_SECRET = '4a269d09d9a04870be65fc4d777bcfae'

fs = Fatsecret(API_ID, API_SECRET)

foods = fs.foods_search('rice')

print(foods)
>>>>>>> dfa83a4ede297e2fbb22031dced60bd8c6ba975c



