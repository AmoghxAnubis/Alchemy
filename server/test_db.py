import requests

# 1. Define the URL
url = "http://127.0.0.1:5000/api/transmute"

# 2. Open the test image we used earlier
files = {'file': open('test.jpg', 'rb')}

# 3. Send the POST request
print("Sending image to the wizard...")
response = requests.post(url, files=files)

# 4. Check results
if response.status_code == 200:
    print("✅ Success! Art generated.")
    
    # 5. Check if it was saved to history
    print("Checking the Grimoire (History)...")
    history_response = requests.get("http://127.0.0.1:5000/api/grimoire")
    history = history_response.json()
    
    print(f"✅ Found {len(history)} spells in the database.")
else:
    print("❌ Failed:", response.text)