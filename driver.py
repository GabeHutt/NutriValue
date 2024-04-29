import diningscrape
import food_database
import maindata
import data_visualizer
import key_table
import json
import os
import time

def delete_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        # File does not exist, so raise an error
        print(f"Error: {file_path} does not exist.")

def main():
    print('Welcome to Brotein')

    while True:
        user_input = input("Enter [1] to populate database (25 items per time), or [2] to initialize the main table: ")
        if user_input == "1":
            print("Populating...")
            diningscrape.main()
            food_database.main()
            time.sleep(8)
            print("25 items populated.")
        elif user_input == "2":
            print("Initializing main table...")
            key_table.main()
            maindata.main()
            
            
            break  # Exit the loop when the main table is initialized
        else:
            print("Invalid input. Please enter [1] to populate or [2] to initialize main tablegit .")
    print("Generating Visualizations")
    while True:
        user_input = input("Enter [1] to quit program: ")
        if user_input == "1":
            delete_file("menu_dict.json")
            delete_file("NutriValue.db")
            delete_file("tracker.json")
            # Reset tracker.json by recreating it immediately after deletion
            with open("tracker.json", 'w') as file:
                json.dump({"name_to_id": 0, "last_id": 0}, file)
            break
            


if __name__ == "__main__":
    main()
