from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# Allow requests from your Vercel frontend
CORS(app, origins=[
    "http://localhost:3000",
    "https://your-app.vercel.app"  # Update after deployment
])

# --- DATABASE CONNECTION ---
# Use environment variable for MongoDB URI
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGODB_URI)
db = client['glitch_wizard']
collection = db['transmutations']

# --- THE ALCHEMY LOGIC ---
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def create_ascii_string(image, new_width=100):
    new_image_data = resize_image(image, new_width)
    gray_image = new_image_data.convert("L")
    new_image_chars = pixels_to_ascii(gray_image)
    
    len_chars = len(new_image_chars)
    ascii_image = "\n".join(
        [new_image_chars[index:(index + new_width)] 
        for index in range(0, len_chars, new_width)]
    )
    return ascii_image

# --- API ROUTES ---

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "alive", "message": "Glitch Wizard API Online"})

@app.route('/api/transmute', methods=['POST'])
def transmute():
    if 'file' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['file']
    
    try:
        image = Image.open(file.stream)
        ascii_art = create_ascii_string(image)
        
        record = {
            "art": ascii_art,
            "created_at": datetime.datetime.utcnow()
        }
        collection.insert_one(record)
        
        return jsonify({"art": ascii_art})
        
    except Exception as e:
        print(e)
        return jsonify({"error": "Transmutation failed"}), 500

@app.route('/api/grimoire', methods=['GET'])
def get_grimoire():
    spells = list(collection.find({}, {'_id': 0}).sort("created_at", -1).limit(10))
    return jsonify(spells)

if __name__ == '__main__':
    app.run(debug=True, port=5000)