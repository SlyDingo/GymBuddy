import json
import os

from storage import storage_manager

# get the absolute path to the storage directory and then create the exercise_master_list file
exercise_master_list = storage_manager.get_file_path_in_storage("exercise_master_list.json", create_if_not_exists=True)

# Get all the existing exericises;
def add_exercise(exerciseID:str, name:str, category:str, variations:list):
    exerciseObject = {
        "exerciseId": exerciseID,
        "name": name,
        "category": category,
        "variations": variations
    }

    json_object = json.dumps(exerciseObject, indent=4)

    with open(exercise_master_list, "w") as file:
        file.write(json_object)
