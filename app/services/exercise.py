class Exercise():
    def __init__(self, exerciseID: str, variation: list[str], category:str) -> None:
        self.exerciseID = exerciseID
        self.variation = variation;
        self.category = category;

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


class Set():
    pass