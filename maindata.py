import sqlite3
import json

dining_hall_names = ['east-quad', 'bursley', 'south-quad', 'markley',
                     'mosher-jordan', 'twigs-at-oxford', 'north-quad'
                     ]
with open("menu_dict.json", 'r') as file:
    menu_dict = json.load(file)

def list_tables_and_columns():
    with sqlite3.connect("NutriValue.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            
                

list_tables_and_columns()


def get_id_from_name(cursor, table, name):
    """
    Helper function to fetch the ID from the database using the name from the respective table.
    """
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None  # Return None if no ID is found

def populate_food_references_with_names(data_dict):
    with sqlite3.connect("NutriValue.db") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS food_references (id INTEGER PRIMARY KEY, hall_name_id INT, course_id INT, meal_id INT)")

        for hall_name, courses_dict in data_dict.items():
            hall_id = get_id_from_name(cursor, 'dining_halls', hall_name)
            if hall_id is None:
                continue
            
            for course_name, food_names in courses_dict.items():
                course_id = get_id_from_name(cursor, 'courses', course_name)
                if course_id is None:
                    continue

                for meal_name in food_names:
                    meal_id = get_id_from_name(cursor, 'food_names', meal_name)
                    if meal_id is None:
                        continue

                    sql_command = """
                        INSERT INTO food_references (hall_name_id, course_id, meal_id)
                        VALUES (?, ?, ?)
                    """
                    try:
                        cursor.execute(sql_command, (hall_id, course_id, meal_id))
                    except sqlite3.IntegrityError:
                        continue

        connection.commit()


# Assuming you have the 'menu_dict' loaded
populate_food_references_with_names(menu_dict)    
        
        
