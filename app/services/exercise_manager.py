import json
import os

from storage import storage_manager

# get the absolute path to the storage directory and then create the exercise_master_list file
exercise_list_json_file_path = storage_manager.get_file_path_in_storage("exercise_list.json", create_if_not_exists=True)

# Get all the existing exericises;
def add_exercise(exerciseID:str, category:str, variations:list[str]) -> None:
    """Add a new exercise to the exercise list JSON file.
    Args:
        exerciseID (str): Unique identifier for the exercise.
        category (str): Category of the exercise (e.g., "Upper-Body", "Lower-Body").
        variations (list): List of variations for the exercise.
    """
    exerciseObject = {
        exerciseID : {
          "category": category,
          "variations": variations
        }
    }

    # Check if the file exists and read existing data
    with open(exercise_list_json_file_path, "r") as file:
        try:
            existing_json_data = json.load(file)
        except json.JSONDecodeError:
            existing_json_data = {}
    
    # append the new exercise object to the existing data
    existing_json_data.update(exerciseObject)

    json_object = json.dumps(existing_json_data, indent=4) # convert object to JSON object

    with open(exercise_list_json_file_path, "w") as file: # write the JSON object to the file
        file.write(json_object)

# Return Dictionary of all exercises
def get_exercise_dictionary() -> dict:
    """Retrieve the dictionary of all exercises from the exercise list JSON file.
    Returns:
        exercise_dict (dict): Dictionary containing all exercises with their details.
    """
    with open(exercise_list_json_file_path, "r") as file:
        try:
            exercise_dict = json.load(file)
        except json.JSONDecodeError:
            exercise_dict = {}
    
    return exercise_dict;