import sqlite3
import json

def populate_food_references_with_joins(data_dict):
    with sqlite3.connect("NutriValue.db") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS food_references (id INTEGER PRIMARY KEY, hall_name_id INT, course_id INT, meal_id INT)")

        
        insert_sql = "INSERT INTO food_references (hall_name_id, course_id, meal_id) VALUES (?, ?, ?)"

        # Iterate over each item in the dictionary
        for hall_name, courses_dict in data_dict.items():
            for course_name, food_names in courses_dict.items():
                for meal_name in food_names:
                    
                    cursor.execute("""
                        SELECT dh.id, c.id, fn.id
                        FROM dining_halls dh
                        JOIN courses c ON c.name = ?
                        JOIN food_names fn ON fn.name = ?
                        WHERE dh.name = ?
                    """, (course_name, meal_name, hall_name))

                    
                    result = cursor.fetchone()
                    if result:
                        hall_id, course_id, meal_id = result
                        try:
                            cursor.execute(insert_sql, (hall_id, course_id, meal_id))
                        except sqlite3.IntegrityError:
                            continue  
                        
        connection.commit()

def main():
    with open("menu_dict.json", 'r') as file:
        menu_dict = json.load(file)
    populate_food_references_with_joins(menu_dict)

if __name__ == '__main__':
    main()
