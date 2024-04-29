import matplotlib.pyplot as plt
import sqlite3
import numpy as np




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
                'num': 0,
            }




    #data collection process
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
                data_collection[hall_id][course_id]['num'] += 1

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
                
    #data compression for visualizations
    dining_protein_scores = [[]]
    for i in range(1, dining_halls.len()):
        for j in range(1, courses.len()):
            dining_protein_scores[i - 1].append = (data_collection[i][j]['p_score']/data_collection[i][j]['num'])
    # set width of bar 
    barWidth = 0.15
    fig = plt.subplots(figsize =(12, 8)) 
 
# set height of bar 
    
 
# Set position of bar on X axis 
    br1 = np.arange(len(dining_protein_scores[0])) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br2] 
    br5 = [x + barWidth for x in br2] 
    br6 = [x + barWidth for x in br2] 
    br7 = [x + barWidth for x in br2] 
 
# Make the plot
    plt.bar(br1, dining_protein_scores[0], color ='r', width = barWidth, 
        edgecolor ='grey', label = dining_halls[1]) 
    plt.bar(br2, dining_protein_scores[1], color ='g', width = barWidth, 
        edgecolor ='grey', label = dining_halls[2]) 
    plt.bar(br3, dining_protein_scores[2], color ='b', width = barWidth, 
        edgecolor ='grey', label = dining_halls[3]) 
    plt.bar(br4, dining_protein_scores[3], color ='o', width = barWidth, 
        edgecolor ='grey', label = dining_halls[4]) 
    plt.bar(br5, dining_protein_scores[4], color ='i', width = barWidth, 
        edgecolor ='grey', llabel = dining_halls[5]) 
    plt.bar(br6, dining_protein_scores[5], color ='v', width = barWidth, 
        edgecolor ='grey', label = dining_halls[6]) 
    plt.bar(br7, dining_protein_scores[6], color ='y', width = barWidth, 
        edgecolor ='grey', label = dining_halls[7]) 
 
# Adding Xticks 
    plt.xlabel('Average Protein Score', fontweight ='bold', fontsize = 15) 
    plt.ylabel('Meal', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(dining_protein_scores[0]))], 
        ['Breakfast', 'Brunch', 'Dinner'])
 
    plt.legend()
    plt.show()  
        







if __name__ == '__main__':
    main()