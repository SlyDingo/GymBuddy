from services import exercise_manager

exercise_manager.add_exercise_type(
    exerciseID="Jumping Jack",
    category="Lower-Body",
    variations=["Bodyweight", "Barbell", "Dumbbell"]
)

set_map = {
    1: {
        "reps": 10,
        "weight": 10,
        "is_warmup": 0,
        "rest_time": 60
    },
    2: {
        "reps": 8,
        "weight": 10,
        "is_warmup": 0,
        "rest_time": 90
    },
    3: {
        "reps": 6,
        "weight": 20,
        "is_warmup": 0,
        "rest_time": 120
    }
}
print("hello world")