import sqlite3
import json

dining_hall_names = ['east-quad', 'bursley', 'south-quad', 'markley',
                     'mosher-jordan', 'twigs-at-oxford', 'north-quad'
                     ]
with open("menu_dict.json", 'r') as file:
    menu_dict = json.load(file)


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
    """
    Populates the 'food_references' table using data from the provided dictionary with names.
    The dictionary is expected to be in the format:
    {
        "hall_name": {"course_name": ["meal_name1", "meal_name2", ...]},
        ...
    }
    """
    with sqlite3.connect("NutriValue.db") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # Ensure the table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_references (
                id INTEGER PRIMARY KEY,
                hall_name_id INTEGER,
                course_id INTEGER,
                meal_id INTEGER,
                FOREIGN KEY(hall_name_id) REFERENCES halls(id),
                FOREIGN KEY(course_id) REFERENCES courses(id),
                FOREIGN KEY(meal_id) REFERENCES meals(id)
            )
        """)

        # Insert data into the table
        for hall_name, courses_dict in data_dict.items():
            hall_id = get_id_from_name(cursor, 'halls', hall_name)
            if hall_id is None:
                print(f"No ID found for hall name '{hall_name}'. Skipping...")
                continue
            
            for course_name, meals in courses_dict.items():
                course_id = get_id_from_name(cursor, 'courses', course_name)
                if course_id is None:
                    print(f"No ID found for course name '{course_name}'. Skipping...")
                    continue

                for meal_name in meals:
                    meal_id = get_id_from_name(cursor, 'meals', meal_name)
                    if meal_id is None:
                        print(f"No ID found for meal name '{meal_name}'. Skipping...")
                        continue

                    try:
                        cursor.execute("""
                            INSERT INTO food_references (hall_name_id, course_id, meal_id)
                            VALUES (?, ?, ?)
                        """, (hall_id, course_id, meal_id))
                    except sqlite3.IntegrityError as e:
                        print(f"Skipping duplicate entry for {hall_name}, {course_name}, {meal_name}: {e}")

        connection.commit()
            



populate_food_references_with_names(menu_dict)      
        
        
