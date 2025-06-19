import json
import os

from storage import storage_manager

# get the absolute path to the storage directory and then create the exercise_master_list file
storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))

print(f"Storage directory: {storage_dir}")
os.makedirs(storage_dir, exist_ok=True)
exercise_master_list = os.path.join(storage_dir, "exercise_master_list.json")

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
