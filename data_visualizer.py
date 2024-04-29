import matplotlib
import sqlite3




#rows[int id][hall name id][course_id][meal_id]

def main():
    enumerate:
        
    connect = sqlite3.connect('NutriValue.db')
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM food_references')  
    rows = cursor.fetchall()
    for row in rows:
        hall_name_id = row[1]
        course_id = row[2]
        meal_id = row[3]
        
        



    connect.close()



if __name__ == '__main__':
    main()