import matplotlib
import sqlite3




#rows[int id][hall name id][course_id][meal_id]

def main():
    dining_halls = [
        'place_holder',
        'East Quad',
        'Bursely',
        'South Quad',
        'Markley',
        'Mosher Jordan',
        'Twigs at Oxford',
        'North Quad'
    ]

    courses = [
        'place_holder',
        'Breakfast',
        'Brunch',
        'Dinner'
    ]

    with sqlite3.connect('NutriValue.db') as connect:
        cursor = connect.cursor() 
        cursor.execute('SELECT * FROM food_references')  
        rows = cursor.fetchall()
        with sqlite3.connect('NutriValue.db') as nutri_connect:
            for row in rows:
                hall_name = dining_halls[row[1]]
                course = courses[row[2]]
                meal_id = row[3]
                nutri_cursor = nutri_connect.cursor()
                nutri_cursor.execute('SELECT fat_score, carb_score, protein_score FROM food_nutrition WHERE food_name_id =?',(meal_id,))

       
        



    connect.close()



if __name__ == '__main__':
    main()