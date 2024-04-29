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

    top_protein_meals = {}
    data_collection = {}
    for i in range(1, dining_halls.len()):
        data_collection[i] = {}
        for j in range(1, courses.len()):
            data_collection[i][j] = {
                'p_score': 0,
                'c_score': 0,
                'f_score': 0,
                'num_p': 0,
                'num_c': 0,
                'num_f': 0
            }





    with sqlite3.connect('NutriValue.db') as connect:
        cursor = connect.cursor() 
        cursor.execute('SELECT * FROM food_references')  
        rows = cursor.fetchall()
        with sqlite3.connect('NutriValue.db') as nutri_connect:
            for row in rows:
                hall_id = row[1]
                course_id = row[2]
                hall_name = dining_halls[hall_id]
                meal_id = row[3]
                nutri_cursor = nutri_connect.cursor()
                nutri_cursor.execute('SELECT fat_score, carb_score, protein_score FROM food_nutrition WHERE food_name_id =?',(meal_id,))
                nutri_scores = nutri_cursor.fetchone()
                if nutri_scores is None:
                    continue
                fat_score = nutri_scores[0]
                protein_score = nutri_scores[2]
                carb_score = nutri_scores[1]
                data_collection[hall_id][course_id]['p_score'] += protein_score
                data_collection[hall_id][course_id]['c_score'] += carb_score
                data_collection[hall_id][course_id]['f_score'] += fat_score
                data_collection[hall_id][course_id]['num_p'] += 1
                data_collection[hall_id][course_id]['num_c'] += 1
                data_collection[hall_id][course_id]['num_f'] += 1

                if hall_name not in top_protein_meals:
                    top_protein_meals[hall_name] = {}
                nutri_cursor.execute('SELECT name FROM food_names WHERE id=?',(meal_id,))
                meal_name_tuple = nutri_cursor.fetchone()
                meal_name = meal_name_tuple[0]
                
                if top_protein_meals[hall_name].len() < 3:
                    if meal_name not in top_protein_meals[hall_name]:
                        top_protein_meals[hall_name][meal_name] = {
                            'p_score': protein_score,
                            'c_score': carb_score,
                            'f_score': fat_score
                        }
                min = 999999999999
                to_remove = None
                if meal_name not in top_protein_meals[hall_name]:
                    for meals in top_protein_meals[hall_name]:
                        current_score = top_protein_meals[meals]['p_score']
                        if protein_score > current_score:
                            if current_score < min:
                                min = current_score
                                to_remove = meals
                    if to_remove != None:
                        top_protein_meals[hall_name].pop(to_remove)
                        top_protein_meals[hall_name][meal_name] = top_protein_meals[hall_name][meal_name] = {
                                'p_score': protein_score,
                                'c_score': carb_score,
                                'f_score': fat_score
                            }
                
                

                
                



       
        



    connect.close()



if __name__ == '__main__':
    main()