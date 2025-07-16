# app.py
from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS # CORS হ্যান্ডেল করার জন্য

app = Flask(__name__)
CORS(app) # CORS সক্ষম করুন যাতে আপনার React অ্যাপ এটি অ্যাক্সেস করতে পারে

@app.route('/')
def home():
    """হোম রুট, সার্ভার চলছে কিনা তা পরীক্ষা করার জন্য।"""
    return "Flask Background Remover Backend is running!"

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    """
    ছবি থেকে ব্যাকগ্রাউন্ড সরানোর জন্য API এন্ডপয়েন্ট।
    React ফ্রন্টএন্ড থেকে ছবি ফাইল গ্রহণ করে এবং স্বচ্ছ ব্যাকগ্রাউন্ড সহ ছবি ফেরত দেয়।
    """
    if 'image_file' not in request.files:
        return {"error": "কোনো 'image_file' পাওয়া যায়নি"}, 400

    image_file = request.files['image_file']

    if not image_file.filename:
        return {"error": "কোনো ফাইল নাম নেই"}, 400

    try:
        # ইনপুট ছবি ডেটা পড়ুন
        input_image_data = image_file.read()

        # rembg ব্যবহার করে ব্যাকগ্রাউন্ড সরান
        output_image_data = remove(input_image_data)

        # PIL (Pillow) ব্যবহার করে ছবি মেমরি থেকে লোড করুন এবং PNG ফরম্যাটে সেভ করুন
        # rembg সাধারণত PNG ফরম্যাটে স্বচ্ছতা সহ আউটপুট দেয়
        output_image_pil = Image.open(io.BytesIO(output_image_data))
        
        # আউটপুট PNG ডেটা মেমরি বাফারে সেভ করুন
        img_byte_arr = io.BytesIO()
        output_image_pil.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0) # বাফারের শুরু থেকে পড়ুন

        # ক্লায়েন্টে প্রসেস করা ছবি পাঠান
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=False, # ব্রাউজারে সরাসরি দেখানোর জন্য
            download_name='no-bg.png'
        )

    except Exception as e:
        print(f"ব্যাকগ্রাউন্ড সরানোর সময় ত্রুটি: {e}")
        return {"error": f"ব্যাকগ্রাউন্ড সরানোর সময় একটি অভ্যন্তরীণ ত্রুটি হয়েছে: {str(e)}"}, 500

if __name__ == '__main__':
    # Flask ডেভেলপমেন্ট সার্ভার রান করুন
    # প্রোডাকশনের জন্য, Gunicorn বা Nginx এর মতো একটি WSGI সার্ভার ব্যবহার করা উচিত।
    app.run(debug=True, port=5000) # পোর্ট 5000 এ রান হবে
