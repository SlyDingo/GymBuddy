import json
import os
import sqlite3

from storage import storage_manager
from .exercise import *


# get the absolute path to the storage directory and then create the exercise_master_list file
exercise_list_json_file_path = storage_manager.get_file_path_in_storage("exercise_list.json", create_if_not_exists=True)
exercise_log_database_file_path = storage_manager.get_file_path_in_storage("exercise_log.db", create_if_not_exists=True)

storage_manager.init_db("exerise", exercise_log_database_file_path)
# Get all the existing exericises;
def add_exercise_type(exerciseID:str, variations:list[str], category:str) -> None:
    """Add a new exercise to the exercise list JSON file.
    Args:
        exerciseID (str): Unique identifier for the exercise.
        category (str): Category of the exercise (e.g., "Upper-Body", "Lower-Body").
        variations (list): List of variations for the exercise.
    """
    
    exerciseObject = Exercise(exerciseID, variations, category)

    # Check if the file exists and read existing data
    storage_manager.ensure_file_exists(exercise_list_json_file_path, "{}")
    with open(exercise_list_json_file_path, "r") as file:
        try:
            existing_json_data = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is empty or corrupted. Initializing with an empty dictionary.")
            existing_json_data = {}
    
    # append the new exercise object to the existing data
    existing_json_data.update(exerciseObject.to_dict(flat=False))

    json_object = json.dumps(existing_json_data, indent=4) # convert object to JSON object

    with open(exercise_list_json_file_path, "w") as file: # write the JSON object to the file
        file.write(json_object)

# Return Dictionary of all exercises
def load_exercise_list() -> list[Exercise]:
    """Load all exercises from the exercise list JSON file."""
    with open(exercise_list_json_file_path, "r") as file:
        try:
            exercise_dict = json.load(file)
        except json.JSONDecodeError:
            exercise_dict = {}
    
    return [Exercise(exerciseID, value["variation"], value["category"]) for exerciseID, value in exercise_dict.items()]

def get_exercise_object(object_to_get:str) -> Exercise:
    """Checks if an type::Exercise exists in the JSON master list.
    If exists returns that object"""
    list_of_exercise = load_exercise_list()
    object_to_get = object_to_get.lower()

    for item in list_of_exercise:
        if (item.name == object_to_get) or (item.exerciseID == object_to_get):
            return item
    
    return Exercise("", [], "")
    
def log_exercise(exerciseObject:Exercise, setMap:SetMap) -> None:
    conn = sqlite3.connect(exercise_log_database_file_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO exercise_log (exercise_id, category, variation, date_unix)
    VALUES (?, ?, ?, ?)
    """, (exerciseObject.exerciseID, exerciseObject.category, exerciseObject.variation[0], 123))

    conn.commit()
    conn.close()

