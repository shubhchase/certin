# utils.py (or any file where you define your utility functions)
import random
import string

def generate_captcha():
    # Generate a random 6-digit number for simplicity
    return ''.join(random.choices(string.digits, k=6))
