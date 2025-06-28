import os

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