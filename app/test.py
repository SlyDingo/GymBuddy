import unittest
import sqlite3
from unittest.mock import patch
import tempfile
import os
import json

from services import exercise_manager
from services.exercise import Exercise, SetMap
from storage import storage_manager

if __name__ == "__main__":
    pass
    
    # path = storage_manager.get_file_path_in_storage("exercise_log.db", False)
    # conn = sqlite3.connect(path)
    # cursor = conn.cursor()

    # exerciseObject = Exercise("bench press", ["barbell"], "upper body")
    # set = SetMap()
    # set.add_set(6, 10, 0)
    # exercise_manager.log_exerise(exerciseObject, set)

    # cursor.execute("""
    # SELECT * FROM exercise_log
    # """)

    # print(cursor.fetchone())

    # cursor.close()
    # conn.close()

    # exerciseObject = Exercise("bench press", ["barbell"], "upper body")
    # set = SetMap()
    # set.add_set(6, 10, 0)
    # exercise_manager.log_exerise(exerciseObject, set)
