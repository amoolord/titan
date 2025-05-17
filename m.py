import os
import json
import time

def get_wifi_list():
    """ دریافت لیست وای‌فای‌های اطراف و نمایش انتخاب عددی """
    result = os.popen("termux-wifi-scaninfo").read()
    if not result.strip():
        print("🚫 هیچ شبکه‌ای یافت نشد! مطمئن شو که وای‌فای روشنه.")
        return []

    wifi_networks = json.loads(result)
    
    if not wifi_networks:
        print("🚫 هیچ شبکه‌ای پیدا نشد!")
        return []

    print("\n📡 لیست شبکه‌های وای‌فای اطراف:\n")
    for index, network in enumerate(wifi_networks, start=1):
        print(f"{index}. {network['ssid']} - قدرت سیگنال: {network['level']} dBm")

    return wifi_networks

def connect_to_wifi(selected_network):
    """ اتصال به وای‌فای (تنها نمایش انتخاب شبکه - اتصال دستی لازم است) """
    print(f"\n✅ شبکه انتخاب‌شده: {selected_network['ssid']}")
    print("🔹 لطفاً به این شبکه به‌صورت دستی متصل شو.")

def toggle_wifi():
    """قطع و وصل وای‌فای هر ۵ ثانیه"""
    os.system("termux-wifi-enable false")  # خاموش کردن وای‌فای
    print("🚫 وای‌فای خاموش شد!")
    time.sleep(2)  # مکث کوتاه
    os.system("termux-wifi-enable true")   # روشن کردن وای‌فای
    print("✅ وای‌فای دوباره فعال شد!")

# دریافت لیست شبکه‌ها
wifi_networks = get_wifi_list()

# درخواست انتخاب شبکه
if wifi_networks:
    try:
        choice = int(input("\n🔢 شماره شبکه موردنظر را وارد کن: ")) - 1
        if 0 <= choice < len(wifi_networks):
            connect_to_wifi(wifi_networks[choice])
        else:
            print("🚫 شماره واردشده نامعتبر است!")
    except ValueError:
        print("🚫 لطفاً عدد معتبر وارد کن!")

# اجرای تست خودکار هر ۵ ثانیه
while True:
    toggle_wifi()
    time.sleep(5)
