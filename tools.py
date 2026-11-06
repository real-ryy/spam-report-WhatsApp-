import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import random

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment jika ingin berjalan tanpa tampilan
    chrome_options.add_argument("--disable-blink-features=Automation")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def send_report(driver, phone_number):
    """Mengirim laporan ke WhatsApp Web"""
    try:
        url = f"https://web.whatsapp.com/report/{phone_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"[+] Laporan terkirim ke {phone_number}")
            return True
        else:
            print(f"[-] Gagal kirim ke {phone_number}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    target_phone = input("Masukkan nomor target (format: 628xxx): ")
    jumlah_laporan = int(input("Berapa kali laporan? "))
    
    print("Menyiapkan driver...")
    driver = setup_driver()
    
    # Buka WhatsApp Web terlebih dahulu untuk login QR Code
    driver.get("https://web.whatsapp.com/send?phone=" + target_phone)
    print("Silakan scan QR Code di jendela Chrome yang terbuka...")
    
    # Tunggu sampai halaman berubah (berarti sudah login)
    while "loading" in driver.page_source.lower():
        time.sleep(1)
        
    print("Login berhasil! Memulai spam...")
    
    for i in range(jumlah_laporan):
        success = send_report(driver, target_phone)
        
        # Random delay agar terlihat seperti manusia
        delay = random.uniform(1, 3)
        time.sleep(delay)
        
        if not success:
            print(f"[!] Terjadi kesalahan pada laporan ke-{i+1}. Mencoba lagi...")
            time.sleep(5)
            
    driver.quit()
    print("Selesai!")

if __name__ == "__main__":
    main()
