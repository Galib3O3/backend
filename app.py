# my-python-backend/app.py

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove, new_session 
from PIL import Image 
import io
import datetime
import pytz 
import sys # sys মডিউল ইম্পোর্ট করুন

app = Flask(__name__)

# CORS সেটআপ
cors_origins = [
    "http://localhost:5173",        
    "https://toolsgovt.netlify.app" # আপনার Netlify ফ্রন্টএন্ড URL
]
CORS(app, resources={r"/*": {"origins": cors_origins}})

# --- ডিবাগ প্রিন্ট স্টেটমেন্ট এবং ত্রুটি হ্যান্ডলিং যোগ করুন ---
print("--- Starting app.py ---")
print(f"Flask app name: {app.name}")
print(f"Current working directory: {os.getcwd()}")
print(f"PORT environment variable: {os.environ.get('PORT')}")

session = None # সেশন ভেরিয়েবলটি গ্লোবালি ইনিশিয়ালাইজ করুন
try:
    print("Attempting to load rembg session (u2net model)...")
    session = new_session("u2net")
    print("Rembg session loaded successfully.")
except Exception as e:
    print(f"!!! CRITICAL ERROR: Failed to load rembg session: {e}", file=sys.stderr) # ত্রুটি স্ট্যান্ডার্ড এরর এ প্রিন্ট করুন
    print("!!! This means the app cannot start. Exiting...", file=sys.stderr)
    sys.exit(1) # অ্যাপটি সাথে সাথে বন্ধ করে দিন যাতে Render ত্রুটিটি ধরতে পারে

# --- আপনার রুট এবং ফাংশনগুলো ---
@app.route('/remove-background', methods=['POST'])
def remove_background():
    # ... (আগের কোড অপরিবর্তিত থাকবে) ...
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    # ...
    try:
        # ... (আগের কোড) ...
        output_image = remove(input_image, session=session) # এখানে session ব্যবহার করুন
        # ... (আগের কোড) ...
    except Exception as e:
        print(f"Error during background removal: {e}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

# লোকাল ডেভেলপমেন্টের জন্য
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    port = int(os.environ.get('PORT', 5000))
    print(f"Local server running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
