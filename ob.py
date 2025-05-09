import hashlib
import socket
import requests

# مشخصات ربات تلگرام
BOT_TOKEN = "8182982379:AAFbB7vFpuCTjH6MHDu7CcZR1nog5grZEWg"
ADMIN_CHAT_ID = "8152202322"  # فقط پیام‌ها به این ID ارسال می‌شوند

def get_user_ip():
    """دریافت آی‌پی کاربر"""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print(f"خطا در دریافت آی‌پی: {e}")
        return None

def hash_ip(ip):
    """هش کردن آی‌پی با SHA256"""
    if ip:
        return hashlib.sha256(ip.encode()).hexdigest()
    return None

def send_to_admin(message):
    """ارسال پیام فقط به ادمین"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": ADMIN_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# اجرا
user_ip = get_user_ip()
if user_ip:
    hashed_ip = hash_ip(user_ip)
    message = f"🔹 آی‌پی جدید ثبت شد:\n{hashed_ip}"
    send_to_admin(message)
    print("✅ آی‌پی هش شده فقط برای ادمین ارسال شد.")
