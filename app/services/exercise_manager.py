import json
import os
import sqlite3

from storage import storage_manager
from exercise import Exercise


# get the absolute path to the storage directory and then create the exercise_master_list file
exercise_list_json_file_path = storage_manager.get_file_path_in_storage("exercise_list.json", create_if_not_exists=True)
exercise_log_database_file_path = os.path.join(storage_manager.get_storage_path(), "exercise_log.db")

# get the absolute path to the storage directory and then create the exercise_log file
log_database = sqlite3.connect(exercise_log_database_file_path);
sql_cursor = log_database.cursor()

sql_cursor.execute('''
CREATE TABLE IF NOT EXISTS exercise_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id TEXT NOT NULL,
        category TEXT NOT NULL,
        variation TEXT NOT NULL,
        date_unix INTEGER NOT NULL
)
''')

log_database.commit()  # Commit the changes to the database

sql_cursor.execute("""
CREATE TABLE IF NOT EXISTS set_log (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  exercise_log_id INTEGER NOT NULL,
                  set_count INTEGER NOT NULL,
                  rep_count INTEGER NOT NULL,
                  weight REAL NOT NULL,
                  is_warmup INTEGER DEFAULT 0,
                  rest_time INTEGER DEFAULT 0,
                  FOREIGN KEY (exercise_log_id) REFERENCES exercise_log (id) ON DELETE CASCADE
                   )
""")

log_database.commit()  # Commit the changes to the database
log_database.close()  # Close the database connection

# Get all the existing exericises;
def add_exercise_type(exerciseID:str, category:str, variations:list[str]) -> None:
    """Add a new exercise to the exercise list JSON file.
    Args:
        exerciseID (str): Unique identifier for the exercise.
        category (str): Category of the exercise (e.g., "Upper-Body", "Lower-Body").
        variations (list): List of variations for the exercise.
    """
    exerciseObject = {
        exerciseID.lower() : {
          "category": category,
          "variations": variations
        }
    }

    exerciseObect = Exercise(exerciseID, variations, category)

    # Check if the file exists and read existing data
    with open(exercise_list_json_file_path, "r") as file:
        try:
            existing_json_data = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is empty or corrupted. Initializing with an empty dictionary.")
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

def log_exercise(exerciseID:str, variation:str, set_map:dict) -> None:
    current_exercise_dict = get_exercise_dictionary()
    if exerciseID not in current_exercise_dict:
        raise ValueError(f"Exercise ID '{exerciseID}' does not exist in the exercise dictionary. Add it.")
    if variation not in current_exercise_dict[exerciseID]["variations"]:
        raise ValueError(f"Variation '{variation}' does not exist for exercise ID '{exerciseID}'. Add it.")
    
    conn = sqlite3.connect(exercise_log_database_file_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO exercise_log (exercise_id, category, variation, date_unix)
    VALUES (?, ?, ?, ?)
    ''', (exerciseID, get_exercise_dictionary()[exerciseID]["category"], variation))
    conn.close()
