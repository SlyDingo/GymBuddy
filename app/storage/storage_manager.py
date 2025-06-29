import os
import sqlite3

def get_storage_path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))

def get_file_path_in_storage(filename:str, create_if_not_exists=True) -> str:                   
    """
    Get the absolute path to a file in the storage directory
    Args:
        filename (str): The name of the file to retrieve
        create_if_not_exists (bool): If True, the directory will be created if it does not exist.                    
                          If False, an exception will be raised if the directory does not exist.
    """
    storage_dir = get_storage_path()

    filename_path = os.path.join(storage_dir, filename)

     # Ensure the storage directory exists and just create the file if it does not exist
    if create_if_not_exists and not os.path.exists(filename_path):
        with open(filename_path, 'w') as f:
            pass

    # Ensure the storage directory exists and if not raise an exception
    if not os.path.exists(storage_dir) and not create_if_not_exists:
        Exception(f"Storage directory '{storage_dir}' does not exist")

    return os.path.join(storage_dir, filename)

def ensure_file_exists(filepath:str, new_file_content:str) -> None:
    """Ensure the file exists. If not, create it with the given content."""
    if not os.path.exists(filepath):
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as file:
            file.write(new_file_content)

def init_exercise_db(path:str):
    # get the absolute path to the storage directory and then create the exercise_log file
    log_database = sqlite3.connect(path);
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

def init_db(database_type:str, path:str) -> None:
    """
    Syntatic Sugar for a more cleaner code. Initialises the chosen databse
    Args:
        database_type (str): filter the type of database function to execute
        path (str): path to said database
    """

    if database_type.lower() == "exercise":
        init_exercise_db(path)