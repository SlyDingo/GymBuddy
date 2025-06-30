import unittest
from unittest.mock import patch
import tempfile
import os
import json
import sqlite3

from services import exercise_manager
from storage import storage_manager
from services.exercise import Exercise, SetMap

join_path = os.path.join
class TestExerciseManager(unittest.TestCase):
    def setUp(self):
        # Create a temporty directory for our unit tets
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_exercise_list_json = join_path(self.temp_dir.name, "exercise_list.json")
        self.temp_exersice_log_db = join_path(self.temp_dir.name, "exercise_log.db")

        # Patch the storage_manager paths used in the module
        self.patcher_json = patch("services.exercise_manager.exercise_list_json_file_path", self.temp_exercise_list_json)
        self.patcher_db = patch("services.exercise_manager.exercise_log_database_file_path", self.temp_exersice_log_db)

        self.patcher_json.start()
        self.patcher_db.start()

        #Cleanup
        self.addCleanup(self.patcher_json.stop)
        self.addCleanup(self.patcher_db.stop)
        self.addCleanup(self.temp_dir.cleanup)


    def tearDown(self):
        # Stop patches and cleanup temp directory
        self.patcher_json.stop()
        self.patcher_db.stop()
        self.temp_dir.cleanup()
    
    #### TESTS ####
    def test_path_in_storage_creates_if_not_exists(self):
        self.assertFalse(os.path.exists(self.temp_exercise_list_json))
        exercise_manager.storage_manager.ensure_file_exists(self.temp_exercise_list_json, "{}")
        self.assertTrue(os.path.exists(self.temp_exercise_list_json))

    def test_added_exercise_exists_in_json(self):
        exercise_manager.add_exercise_type(exerciseID="Bench Press", category="Upper Body", variations=["Barbell", "Dumbell"])

        with open(self.temp_exercise_list_json, "r") as file:
            data = json.load(file)
        
        self.assertIn("bench press", data) # Check if it lowercases the exerciseID
        self.assertEqual(data["bench press"]["category"], "upper body")
        self.assertListEqual(data["bench press"]["variation"], ["barbell", "dumbell"])

    def test_exercise_class(self):
        exer_obj = Exercise("bench press", ["barbell"], "upper body")
        exer_obj.add_to_registry()

        self.assertIn(exer_obj.exerciseID, Exercise.registiry)
        self.assertEqual(exer_obj, Exercise.get(exer_obj.exerciseID))
        self.assertTrue(Exercise.exists(exer_obj.exerciseID))

        obj = Exercise("bro press", ["Dumbell"], "upper body")
        Exercise.add(obj)

        self.assertIn(obj.exerciseID, Exercise.registiry)
        self.assertEqual(obj, Exercise.get(obj.exerciseID))

    def test_get_exercise_object(self):
        exercise_manager.add_exercise_type(exerciseID="Bench Press", category="Upper Body", variations=["Barbell", "Dumbell"])
        item_to_check = exercise_manager.get_exercise("Bench Press")
        self.assertEqual(item_to_check.exerciseID, "bench press")
        self.assertEqual(item_to_check.category, "upper body")
        self.assertEqual(item_to_check.variation, ["barbell", "dumbell"])
    
    def test_logging_exercise_into_database(self):
        storage_manager.init_db("Exercise", exercise_manager.exercise_log_database_file_path)
        exerciseObject = Exercise("bench press", ["barbell"], "upper body")
        set = SetMap()
        set.add_set(6, 10, 0)
        exercise_manager.log_exercise(exerciseObject, set)

        conn = sqlite3.connect(self.temp_exersice_log_db)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM exercise_log
        """)

        self.assertEqual(cursor.fetchone(), (1, 'bench press', 'upper body', 'barbell', 123))

        cursor.close()
        conn.close()



if __name__ == "__main__":
    unittest.main()

