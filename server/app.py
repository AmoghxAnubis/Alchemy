from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# --- THE ALCHEMY CONSTANTS ---
# A gradient of characters from Dark (dense) to Light (sparse)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# --- THE SPELL LOGIC ---

def resize_image(image, new_width=100):
    """
    Shrinks the image.
    We multiply height by 0.55 because terminal characters 
    are usually twice as tall as they are wide.
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.65
)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    """
    Converts the image to black and white (L mode).
    """
    return image.convert("L")

def pixels_to_ascii(image):
    """
    Maps every pixel to a character from our ASCII_CHARS list.
    """
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def create_ascii_string(image, new_width=100):
    """
    The Master Spell: Combines all steps.
    """
    # 1. Resize
    new_image_data = resize_image(image, new_width)
    # 2. Grayscale
    gray_image = grayscale_image(new_image_data)
    # 3. Map to Characters
    new_image_chars = pixels_to_ascii(gray_image)
    
    # 4. Format: Break the long string into lines
    len_chars = len(new_image_chars)
    ascii_image = "\n".join(
        [new_image_chars[index:(index + new_width)] 
        for index in range(0, len_chars, new_width)]
    )
    
    return ascii_image

# --- THE API ROUTES ---

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "alive", "message": "Glitch Wizard Ready."})

@app.route('/api/transmute', methods=['POST'])
def transmute():
    # Check if a file was sent
    if 'file' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['file']
    
    try:
        # Open the image directly from the request stream
        image = Image.open(file.stream)
        
        # Cast the spell
        ascii_art = create_ascii_string(image)
        
        return jsonify({"art": ascii_art})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)