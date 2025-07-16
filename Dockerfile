# একটি হালকা ওজনের পাইথন বেস ইমেজ ব্যবহার করুন
FROM python:3.9-slim-buster

# কাজের ডিরেক্টরি সেট করুন
WORKDIR /app

# প্রয়োজনীয় ফাইলগুলো কপি করুন
COPY requirements.txt .
COPY app.py .

# পাইথন নির্ভরতাগুলো ইন্সটল করুন
RUN pip install --no-cache-dir -r requirements.txt

# Gunicorn সার্ভার ব্যবহার করে অ্যাপ রান করার কমান্ড
# Gunicorn একটি প্রোডাকশন-গ্রেড WSGI HTTP সার্ভার
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
# --bind :$PORT: Cloud Run স্বয়ংক্রিয়ভাবে PORT এনভায়রনমেন্ট ভেরিয়েবল সেট করে।
# --workers 1: একটি ওয়ার্কার (ফ্রি টায়ারের জন্য যথেষ্ট)
# --threads 8: কনকারেন্ট রিকোয়েস্ট হ্যান্ডেল করার জন্য থ্রেড
# --timeout 0: রিকোয়েস্টের জন্য কোনো টাইমআউট নেই (ছবি প্রসেস হতে সময় লাগতে পারে)
# app:app: app.py ফাইল থেকে 'app' Flask অ্যাপ্লিকেশন ইনস্ট্যান্স
