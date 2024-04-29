from diningscrape import dining_hall_names
import sqlite3



def write_dining_hall_to_id():
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS dining_halls (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")

        for dining_hall in dining_hall_names:
            try:
                curr.execute("INSERT INTO dining_halls (name) VALUES (?)", (dining_hall,))
            except sqlite3.IntegrityError:
                # Skip duplicate dining hall silently
                continue

        connection.commit()

def write_course_to_id():
    courses = ['breakfast', 'brunch', 'dinner']
    with sqlite3.connect("NutriValue.db") as connection:
        curr = connection.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")

        for course in courses:
            try:
                curr.execute("INSERT INTO courses (name) VALUES (?)", (course,))
            except sqlite3.IntegrityError:
                # Skip duplicate course silently
                continue

        connection.commit()

write_dining_hall_to_id()
write_course_to_id()