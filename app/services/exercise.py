#TODO
# add __Str__ method to Exercise class

class Exercise():
    registiry = {} # Tracks all instances of the exercise

    def __init__(self, exerciseID: str, variation: list[str], category:str) -> None:
        self.name = exerciseID
        self.exerciseID = exerciseID.lower()
        # self.name = exerciseID
        self.variation = [item.lower() for item in variation];
        self.category = category.lower();

        Exercise.registiry[self.exerciseID] = self  # adds a strong reference

    def add_to_registry(self) -> None:
        """Adds a strong reference to self by adding it to a registry list"""
        Exercise.add(self)
    
    def to_dict(self, flat=True) -> dict:
        """Convert the Exercise object to a dictionary."""
        if not flat: # good for fast lookup by exerciseID
            return {
                self.exerciseID : {
                    "variation": self.variation,
                    "category": self.category
                }
            }
        
        return {
            "exerciseID": self.exerciseID,
            "variation": self.variation,
            "category": self.category
        }

    @classmethod
    def add(cls, exercise:'Exercise') -> None:
        cls.registiry[exercise.exerciseID] = exercise  # Adds a strong reference to the registry

    @classmethod
    def exists(cls, exerciseID_to_check:str) -> bool:
        """Check to see if the exercise Objects exists """
        for name in cls.registiry:
            if (exerciseID_to_check.lower() == name):
                return True

        return False
    
    @classmethod
    def get(cls, exerciseID_to_get:str) -> 'Exercise':
        """Returns an instance of Exercise if it exists in the registry"""
        exerciseID_to_get = exerciseID_to_get.lower()
        if cls.exists(exerciseID_to_get):
            return cls.registiry[exerciseID_to_get]
        
        raise ValueError(f"Exercise with ID '{exerciseID_to_get}' does not exist in the registry.")
    
    @classmethod
    def remove(cls, exerciseID_to_remove) -> None:
        """Removes an instance of Exercise from the registry"""
        cls.registiry.pop(exerciseID_to_remove.lower())
    
    @classmethod
    def _to_dict(cls, flat=True) -> dict:
        dict_to_return = {}
        for exercise in cls.registiry:
            dict_to_return.update(exercise.to_dict(flat=False))
        
        return dict_to_return
    
    # @classmethod
    # def add(cls, exercise) -> None:
    #     cls.registiry[exercise.exerciseID] = exercise

class SetMap():
    """Store the Workout data for a specific workout"""
    set_map = []
    total_sets = 0;

    def __init__(self) -> None:
        pass

    def add_set(self, rep_count:int, weight:float, is_warmup=0) -> None:
        self.set_map.append({
            "rep": rep_count,
            "weight": weight,
            "is_warmup": is_warmup
        })

        self.total_sets += 1

class ExerciseLog(SetMap):
    def __init__(self, exerciseID:str, variation:str, category:str) -> None:
        super().__init__()
        self.exerciseID = exerciseID.lower()
        self.variation = variation
        self.category = category

        # Check if Exercise exists in all existing Exercises
        if not Exercise.exists(self.exerciseID):
            raise ValueError("Exercie does not exist")
