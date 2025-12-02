from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from pymongo import MongoClient
import datetime
import io

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
# 1. Connect to the local MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# 2. Create/Select the database "glitch_wizard"
db = client['glitch_wizard']

# 3. Create/Select the collection "transmutations"
collection = db['transmutations']

# --- THE ALCHEMY LOGIC (Same as before) ---
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
    return jsonify({"status": "alive", "message": "Glitch Wizard Connected to DB."})

@app.route('/api/transmute', methods=['POST'])
def transmute():
    if 'file' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['file']
    
    try:
        image = Image.open(file.stream)
        ascii_art = create_ascii_string(image)
        
        # --- NEW: SAVE TO DATABASE ---
        record = {
            "art": ascii_art,
            "created_at": datetime.datetime.utcnow()
        }
        # Insert into MongoDB
        collection.insert_one(record)
        
        return jsonify({"art": ascii_art})
        
    except Exception as e:
        print(e)
        return jsonify({"error": "Transmutation failed"}), 500

@app.route('/api/grimoire', methods=['GET'])
def get_grimoire():
    # --- NEW: FETCH HISTORY ---
    # 1. Find all records
    # 2. Exclude '_id' (because ObjectId isn't JSON friendly by default)
    # 3. Sort by newest first (-1)
    # 4. Limit to last 10
    spells = list(collection.find({}, {'_id': 0}).sort("created_at", -1).limit(10))
    
    return jsonify(spells)

if __name__ == '__main__':
    app.run(debug=True, port=5000)