import time
import random

# List of relaxation techniques
relaxation_tips = [
    "Try deep breathing: Inhale for 4 seconds, hold for 4 seconds, exhale for 6 seconds. Repeat 5 times.",
    "Close your eyes and visualize a peaceful place. Imagine yourself there for a few minutes.",
    "Stretch your body slowly. Loosen your shoulders, neck, and hands.",
    "Listen to calming music or nature sounds to relax your mind.",
    "Drink a glass of water and take a moment to slow down.",
]

def get_relaxation_tip():
    """Returns a random relaxation technique."""
    return random.choice(relaxation_tips)

def guided_breathing():
    """A simple breathing exercise using text-based guidance."""
    print("\n🧘‍♂️ Guided Breathing Exercise 🧘‍♀️\n")
    for i in range(3):
        print("Inhale... 🫁 (4 seconds)")
        time.sleep(4)
        print("Hold... ✋ (4 seconds)")
        time.sleep(4)
        print("Exhale... 😌 (6 seconds)")
        time.sleep(6)
    print("\nFeel better? Take a moment to relax! 😊\n")
