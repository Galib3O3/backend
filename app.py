# image-bg-remover-backend/app.py

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove, new_session # rembg লাইব্রেরি
from PIL import Image # Pillow ইমেজ প্রসেসিং এর জন্য
import io

app = Flask(__name__)

# CORS সেটআপ: আপনার ফ্রন্টএন্ডের URL গুলো এখানে যোগ করুন
# Render এ deploy হওয়ার পর এটি আপনার Netlify App এর URL থেকে রিকোয়েস্ট গ্রহণ করবে
cors_origins = [       # লোকাল ডেভেলপমেন্টের জন্য
    "https://toolsgovt.netlify.app" # <-- আপনার Netlify ফ্রন্টএন্ড URL এখানে যোগ করুন
    # যদি আপনার ফ্রন্টএন্ড অন্য কোনো URL এ হোস্ট করা হয়, সেগুলো এখানে যোগ করুন
]
CORS(app, resources={r"/*": {"origins": cors_origins}}) # সকল রুটের জন্য CORS

# rembg মডেল লোড করুন (একবার লোড করলে দ্রুত হবে)
# বিভিন্ন মডেল আছে, যেমন 'u2net', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use'
# 'u2net' একটি সাধারণ এবং ভালো কাজ করে।
session = new_session("u2net") 

# রুট: /remove-background (POST রিকোয়েস্ট হ্যান্ডেল করবে)
@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if image_file:
        try:
            # ইনপুট ইমেজ ডেটা পড়ুন
            input_image_bytes = image_file.read()
            input_image = Image.open(io.BytesIO(input_image_bytes)).convert("RGBA")

            # rembg ব্যবহার করে ব্যাকগ্রাউন্ড সরান
            output_image = remove(input_image, session=session)

            # আউটপুট ইমেজকে bytes এ কনভার্ট করুন
            output_image_bytes_io = io.BytesIO()
            output_image.save(output_image_bytes_io, format="PNG")
            output_image_bytes_io.seek(0) # বাইটস্ট্রিম শুরুতে নিয়ে আসা

            # ইমেজ ফাইল হিসাবে ফেরত পাঠান
            return send_file(
                output_image_bytes_io,
                mimetype="image/png",
                as_attachment=False, # ব্রাউজারে সরাসরি ইমেজ দেখানোর জন্য
                download_name="no_background.png"
            )

        except Exception as e:
            print(f"Error during background removal: {e}")
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500
    
    return jsonify({"error": "Something went wrong"}), 500

# লোকাল ডেভেলপমেন্টের জন্য সার্ভার চালু
# Render এ deploy করার সময় এটি gunicorn দ্বারা প্রতিস্থাপিত হবে
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv() # লোকালি .env ফাইল লোড করবে
    
    # Render পরিবেশ থেকে PORT পাবে, না হলে 5000 ব্যবহার করবে
    port = int(os.environ.get('PORT', 5000))
    print(f"Server running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
