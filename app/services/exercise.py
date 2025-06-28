#TODO
# add __Str__ method to Exercise class

class Exercise():
    def __init__(self, exerciseID: str, variation: list[str], category:str) -> None:
        self.name = exerciseID
        self.exerciseID = exerciseID.lower()
        # self.name = exerciseID
        self.variation = [item.lower() for item in variation];
        self.category = category.lower();

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
