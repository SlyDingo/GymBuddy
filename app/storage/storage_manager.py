import os

def get_storage_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))

def get_file_path(filename, create_if_not_exists=True):
    storage_path = get_storage_path()

     # Ensure the storage directory exists
    if not os.path.exists(storage_path) and create_if_not_exists:
        os.makedirs(storage_path)
        

    # Ensure the storage directory exists
    if not os.path.exists(storage_path):
        Exception(f"Storage directory '{storage_path}' does not exist")

    return os.path.join(storage_path, filename)