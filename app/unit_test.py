import unittest
from unittest.mock import patch
import tempfile
import os
import json
# import os
# import tempfile
# from unittest.mock import patch

from services import exercise_manager
from storage import storage_manager
# from services.exercise import Exercise

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

    def test_get_exercise_object(self):
        exercise_manager.add_exercise_type(exerciseID="Bench Press", category="Upper Body", variations=["Barbell", "Dumbell"])
        item_to_check = exercise_manager.get_exercise_object("Bench Press")
        self.assertEqual(item_to_check.exerciseID, "bench press")
        self.assertEqual(item_to_check.category, "upper body")
        self.assertEqual(item_to_check.variation, ["barbell", "dumbell"])


if __name__ == "__main__":
    unittest.main()

