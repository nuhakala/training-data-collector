"""
This Module contains TrainingType class, Enum for all available
training-categories and constant-list of all available training-types.
"""

from Category import Cat


class TrainingType:
    categories = []
    name = ""
    shorthands = []

    def __init__(self, name, categories, shorthands) -> None:
        self.categories = categories
        self.name = name
        self.shorthands = shorthands


TRAIN_TYPES = [
    TrainingType(
        "Juoksu",
        [
            Cat.DURATION,
            Cat.DISTANCE,
            Cat.HEART_RATE_AVG,
            Cat.HEART_RATE_MAX,
            Cat.SPEED,
            Cat.STRENGTH_ESTIMATE,
            Cat.FEELING_ESTIMATE,
            Cat.DESCRIPTION,
            Cat.SAVE,
            Cat.DATE,
        ],
        ["j"],
    ),
    TrainingType(
        "Sali ylävartalo",
        [
            Cat.DURATION,
            Cat.HEART_RATE_AVG,
            Cat.HEART_RATE_MAX,
            Cat.STRENGTH_ESTIMATE,
            Cat.FEELING_ESTIMATE,
            Cat.DESCRIPTION,
            Cat.SAVE,
            Cat.DATE,
        ],
        ["y"],
    ),
    TrainingType(
        "Sali jalat",
        [
            Cat.DURATION,
            Cat.HEART_RATE_AVG,
            Cat.HEART_RATE_MAX,
            Cat.STRENGTH_ESTIMATE,
            Cat.FEELING_ESTIMATE,
            Cat.DESCRIPTION,
            Cat.SAVE,
            Cat.DATE,
        ],
        ["a"],
    ),
    TrainingType(
        "Hiihto",
        [
            Cat.DURATION,
            Cat.DISTANCE,
            Cat.HEART_RATE_AVG,
            Cat.HEART_RATE_MAX,
            Cat.SPEED,
            Cat.STRENGTH_ESTIMATE,
            Cat.FEELING_ESTIMATE,
            Cat.DESCRIPTION,
            Cat.SAVE,
            Cat.DATE,
        ],
        ["h"],
    ),
    TrainingType(
        "Kävely",
        [
            Cat.DURATION,
            Cat.DISTANCE,
            Cat.HEART_RATE_AVG,
            Cat.HEART_RATE_MAX,
            Cat.STRENGTH_ESTIMATE,
            Cat.FEELING_ESTIMATE,
            Cat.DESCRIPTION,
            Cat.SAVE,
            Cat.DATE,
        ],
        ["k"],
    ),
]
