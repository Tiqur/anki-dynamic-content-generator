import random


def generate_card():
    front = f"Front: {random.randint(1, 100)}"
    back = f"Front: {random.randint(1, 100)}"
    return front, back
