import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
# Uses Railway's MONGO_URL variable. Fallback to local if not found.
MONGO_URI = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/alchemy_db')

try:
    client = MongoClient(MONGO_URI)
    # Get the default database from the URI
    db = client.get_database() 
    spells_collection = db.spells
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    spells_collection = None

# --- THE ALCHEMY CONSTANTS ---
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# --- THE SPELL LOGIC ---

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.65)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def create_ascii_string(image, new_width=100):
    new_image_data = resize_image(image, new_width)
    gray_image = grayscale_image(new_image_data)
    new_image_chars = pixels_to_ascii(gray_image)
    
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

@app.route('/api/grimoire', methods=['GET'])
def get_grimoire():
    if spells_collection is None:
        return jsonify([])
    
    # Fetch last 10 spells, newest first. 
    # Exclude _id because it's not JSON serializable by default
    history = list(spells_collection.find({}, {'_id': 0}).sort('_id', -1).limit(10))
    return jsonify(history)

@app.route('/api/transmute', methods=['POST'])
def transmute():
    if 'file' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['file']
    
    try:
        image = Image.open(file.stream)
        ascii_art = create_ascii_string(image)
        
        # Save to DB if connected
        if spells_collection is not None:
            spells_collection.insert_one({"art": ascii_art})
        
        return jsonify({"art": ascii_art})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use the PORT environment variable provided by the deployment platform
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)