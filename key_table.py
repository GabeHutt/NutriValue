from diningscrape import dining_hall_names
import sqlite3



def write_dining_hall_to_id():
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS dining_halls (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")

        for dining_hall in dining_hall_names:
            curr.execute("INSERT INTO dining_halls (name) VALUES (?)", (dining_hall,))

def write_course_to_id():
    courses = ['breakfast', 'brunch', 'dinner']
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")

        for course in courses:
            curr.execute("INSERT INTO courses (name) VALUES (?)", (course,))

write_dining_hall_to_id()
write_course_to_id()