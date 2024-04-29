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
    for i in range(1, len(dining_halls)):
        data_collection[i] = {}
        for j in range(1, len(courses)):
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
                
                if len(top_protein_meals[hall_name]) < 3:
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
                        current_score = top_protein_meals[hall_name][meals]['p_score']
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
                
    data_dining_halls = [
        'East Quad',
        'Bursely',
        'South Quad',
        'Markley',
        'Mosher Jordan',
        'Twigs at Oxford',
        'North Quad'
    ]
    data_courses = [
        'Breakfast',
        'Brunch',
        'Dinner'
    ]
    # Data compression for visualizations
    
    # Set width of bar
    barWidth = 0.1
    fig, axs = plt.subplots(3, 1)

    # Set position of bar on X axis
    r = np.arange(3)

    # Define a color map
    colors = ["#1984c5", "#63bff0", "#a7d5ed", "#e2e2e2", "#e1a692", "#e14b31", "#c23728"]

    # Protein Score Plot
    dining_protein_scores = []
    for i in range(1, len(dining_halls)):
        scores = [data_collection[i][j]['p_score'] / data_collection[i][j]['num'] for j in range(1,len(courses))]
        dining_protein_scores.append(scores)
    for i, dining_hall in enumerate(data_dining_halls):
        axs[0].bar(r + i * barWidth, dining_protein_scores[i], color = colors[i], width = barWidth, label = dining_hall)


    axs[0].set_ylabel('Average Protein %', fontweight='bold', fontsize=15)
    axs[0].set_xticks([r + 3*barWidth for r in range(len(data_courses))], data_courses)
    axs[0].set_yticks([0, 20, 40, 60, 80, 100])

   
    

    #Now visualizing data for carb scores
    
    dining_carb_scores = []
    for i in range(1, len(dining_halls)):
        scores = [data_collection[i][j]['c_score'] / data_collection[i][j]['num'] for j in range(1,len(courses))]
        dining_carb_scores.append(scores)

    for i, dining_hall in enumerate(data_dining_halls):
        axs[1].bar(r + i * barWidth, dining_carb_scores[i], color = colors[i], width = barWidth, label = dining_hall)


    axs[1].set_ylabel('Average Carb %', fontweight='bold', fontsize=15)
    axs[1].set_xticks([r + 3*barWidth for r in range(len(data_courses))], data_courses)
    axs[1].set_yticks([0, 20, 40, 60, 80, 100])

 
    


    #Fat Score Visualizing
    dining_fat_scores = []
    for i in range(1, len(dining_halls)):
        scores = [data_collection[i][j]['f_score'] / data_collection[i][j]['num'] for j in range(1,len(courses))]
        dining_fat_scores.append(scores)
    for i, dining_hall in enumerate(data_dining_halls):
        axs[2].bar(r + i * barWidth, dining_fat_scores[i], color = colors[i], width = barWidth, label = dining_hall)


    axs[2].set_xlabel('Meal', fontweight='bold', fontsize=15)
    axs[2].set_ylabel('Average Fat %', fontweight='bold', fontsize=15)
    axs[2].set_xticks([r + 3*barWidth for r in range(len(data_courses))], data_courses)
    axs[2].set_yticks([0, 20, 40, 60, 80, 100])

    fig.legend(data_dining_halls, title='Dining Halls', loc='center left', bbox_to_anchor=(0.025, 0.5))
    fig.subplots_adjust(left=0.2)
    plt.show()

    
    

if __name__ == '__main__':
    main()    




