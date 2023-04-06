import random

FIRST_WORD = [
    "Blue",
    "Cyan",
    "Epsilion",
    "Echo",
    "Gold",
    "Green",
    "Grey",
    "Red",
]

SECOND_WORD = [
    "Leader",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve"
]

def random_call_sign() -> str:
    """Generate a random call sign"""
    return f"{random.choice(FIRST_WORD)} {random.choice(SECOND_WORD)}"
