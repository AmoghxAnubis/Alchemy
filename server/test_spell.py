# test_spell.py
from PIL import Image
from app import create_ascii_string

# Load the image
try:
    image = Image.open("test.jpg")
    # Generate the art
    art = create_ascii_string(image)
    # Print it to the terminal
    print(art)
except FileNotFoundError:
    print("Error: Please put a 'test.jpg' file in this folder first!")