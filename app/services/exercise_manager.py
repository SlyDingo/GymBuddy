import json

def add_exerise(exerciseID:str, name:str, category:str, variations:list):
    exerciseObject = {
        "exerciseId": exerciseID,
        "name": name,
        "category": category,
        "variations": variations
    }
