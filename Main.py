import os
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Paylaştığın Telegram bilgileri doğrudan koda entegre edildi
TELEGRAM_TOKEN = "8249167686:AAFH5-QP9l-H6fHheiCK_FnlBFgpPXeBYZA"
CHAT_ID = "6322020905"

# Railway'in port yönetimini dinamik olarak yapabilmesi için gerekli ayar
PORT = int(os.environ.get("PORT", 5000))

def telegram_bildirim_gonder(mesaj):
    """Giriş yapan IP bilgilerini Telegram'a gönderen fonksiyon"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram bildirimi gönderilemedi: {e}")

@app.route('/')
def home():
    # Kullanıcının gerçek IP adresini yakalıyoruz
    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    # Giriş yapılan anın tarih ve saat bilgisi
    su_an = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Telegram botunun sana göndereceği mesaj taslağı
    bildirim_metni = f"🚨 *Yeni Ziyaretçi Girişi!*\n\n" \
                     f"🌐 *IP Adresi:* `{user_ip}`\n" \
                     f"⏰ *Zaman:* {su_an}\n" \
                     f"📄 *Konum:* Ana Sayfa"
    
    telegram_bildirim_gonder(bildirim_metni)
    
    return "Sitemize Hoş Geldiniz!"

if __name__ == '__main__':
    # Railway ve dış dünya erişimi için host '0.0.0.0' olmalıdır
    app.run(host='0.0.0.0', port=PORT)
