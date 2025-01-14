import requests
import time
from datetime import datetime, timedelta
import platform
import os
from bs4 import BeautifulSoup
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Terminal renk kodları
class TerminalColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

# URL'ler
VISA_URLS = {
    'italy': {
        'base': 'https://www.idata.com.tr/ita/tr',
        'ankara': 'https://www.idata.com.tr/ita/tr/ankara-randevu',
        'istanbul': 'https://www.idata.com.tr/ita/tr/istanbul-randevu'
    },
    'spain': {
        'base': 'https://turkey.blsspainvisa.com',
        'ankara': 'https://turkey.blsspainvisa.com/appointment/slots',
        'istanbul': 'https://turkey.blsspainvisa.com/appointment/slots'
    }
}

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    """Telegram üzerinden mesaj gönder"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram bildirimleri için TOKEN ve CHAT_ID gerekli!")
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info("Telegram bildirimi gönderildi")
    except Exception as e:
        logger.error(f"Telegram mesajı gönderilemedi: {e}")

def play_notification_sound():
    """Sistem sesli uyarı çal"""
    try:
        if platform.system() == 'Darwin':  # macOS
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif platform.system() == 'Windows':
            import winsound
            winsound.Beep(1000, 1000)
        else:  # Linux
            os.system('beep')
        logger.info("Sesli bildirim çalındı")
    except Exception as e:
        logger.error(f"Sesli bildirim çalınamadı: {e}")

def extract_appointment_details(html, country):
    """En yakın randevu tarihini bul"""
    soup = BeautifulSoup(html, 'html.parser')
    
    if country == 'italy':
        # iData için randevu tarihlerini bul
        available_dates = soup.find_all('td', class_='day')
        dates = []
        
        for date in available_dates:
            if not date.get('class') or 'disabled' not in date.get('class'):
                date_text = date.get_text(strip=True)
                if date_text and date_text != '':
                    dates.append(date_text)
        
        if dates:
            return [f"En yakın randevu tarihi: {dates[0]}"]
    
    elif country == 'spain':
        # BLS için randevu tarihlerini bul
        dates = []
        
        # Önce tarih seçim alanını bul
        date_select = soup.find('select', {'name': 'appointment_date'})
        if date_select:
            available_dates = date_select.find_all('option')
            for date in available_dates:
                if date.get('value') and date.get('value') != '':
                    dates.append(date.get_text(strip=True))
        
        # Eğer tarih seçim alanı yoksa, sayfa içindeki tarihleri ara
        if not dates:
            date_elements = soup.find_all(['div', 'span'], string=lambda text: text and any(month in text.lower() for month in ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık']))
            for date in date_elements:
                date_text = date.get_text(strip=True)
                if date_text and not any(x in date_text.lower() for x in ['no slots', 'no appointment']):
                    dates.append(date_text)
        
        if dates:
            return [f"En yakın randevu tarihi: {dates[0]}"]
    
    return ["Randevu var! Lütfen hemen siteyi kontrol edin."]

def check_appointment(country, city):
    """Randevu kontrolü yap"""
    url = VISA_URLS[country][city]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': VISA_URLS[country]['base'],
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        logger.info(f"Kontrol ediliyor: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        logger.info(f"Durum Kodu: {response.status_code}")
        
        html = response.text
        html_lower = html.lower()
        
        # İtalya için kontrol
        if country == 'italy':
            if 'randevu bulunmamaktadır' not in html_lower and 'no appointment available' not in html_lower:
                details = extract_appointment_details(html, country)
                return True, details
        
        # İspanya için kontrol
        elif country == 'spain':
            if 'no slots available' not in html_lower and 'no appointment available' not in html_lower:
                details = extract_appointment_details(html, country)
                return True, details
        
        return False, []
        
    except requests.exceptions.ConnectionError:
        error_msg = "Site bağlantısı başarısız oldu. İnternet bağlantınızı kontrol edin."
        logger.error(error_msg)
        return False, [error_msg]
    except requests.exceptions.Timeout:
        error_msg = "Site yanıt vermiyor (timeout). Daha sonra tekrar deneyin."
        logger.error(error_msg)
        return False, [error_msg]
    except Exception as e:
        error_msg = f"Beklenmeyen bir hata oluştu: {str(e)}"
        logger.error(error_msg)
        return False, [error_msg]

def main():
    logger.info("Bot başlatılıyor...")
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("""
        ⚠️ Telegram bildirimleri için gerekli bilgiler eksik!
        Lütfen .env dosyasında şu değişkenleri tanımlayın:
        TELEGRAM_BOT_TOKEN=your_bot_token
        TELEGRAM_CHAT_ID=your_chat_id
        """)
        input("Devam etmek için Enter'a basın...")
    
    print("\nSchengen Turist Vizesi Randevu Kontrol Botu")
    print("------------------------------------------")
    print("\nNot: Bu bot sadece turist vizesi randevularını kontrol eder!")
    
    # Ülke seçimi
    print("\nÜlke seçin:")
    print("1. İtalya")
    print("2. İspanya")
    country = input("Seçiminiz (1/2): ")
    country = 'italy' if country == '1' else 'spain'
    
    # Şehir seçimi
    print("\nŞehir seçin:")
    print("1. Ankara")
    print("2. İstanbul")
    city = input("Seçiminiz (1/2): ")
    city = 'ankara' if city == '1' else 'istanbul'
    
    # Kontrol tipi seçimi
    print("\nKontrol tipi seçin:")
    print("1. Sürekli kontrol")
    print("2. Belirli aralıklarla kontrol")
    check_type = input("Seçiminiz (1/2): ")
    
    # Kontrol sıklığı
    interval = 1  # Varsayılan 1 saniye
    if check_type == '2':
        interval = int(input("\nKontrol sıklığı (dakika): ")) * 60  # Dakikayı saniyeye çevir
    
    logger.info(f"\n{country.upper()} - {city.upper()} için randevu kontrolü başlıyor...")
    logger.info(f"Kontrol tipi: {'Sürekli' if check_type == '1' else f'Her {interval//60} dakikada bir'}")
    print("\nBotu durdurmak için Ctrl+C tuşlarına basın")
    
    error_count = 0
    max_errors = 3
    
    try:
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            logger.info(f"[{now}] Kontrol yapılıyor...")
            
            has_appointment, details = check_appointment(country, city)
            if has_appointment:
                # Terminal için renkli mesaj
                terminal_message = f"""
🎉 RANDEVU BULUNDU!

🌍 Ülke: {country.upper()}
🏢 Şehir: {city.upper()}
⏰ Kontrol Zamanı: {now}

📝 Detaylar:
{chr(10).join(f'- {detail}' for detail in details)}

🔗 Site: {VISA_URLS[country][city]}

⚡️ Lütfen hemen siteye giriş yapın ve randevuyu alın!
                """
                
                # Telegram için renksiz mesaj
                telegram_message = f"""
🎉 RANDEVU BULUNDU!

🌍 Ülke: {country.upper()}
🏢 Şehir: {city.upper()}
⏰ Kontrol Zamanı: {now}

📝 Detaylar:
{chr(10).join(f'- {detail}' for detail in details)}

🔗 Site: {VISA_URLS[country][city]}

⚡️ Lütfen hemen siteye giriş yapın ve randevuyu alın!
                """
                
                logger.info("Randevu bulundu! Bildirimler gönderiliyor...")
                play_notification_sound()
                send_telegram_message(telegram_message)
                
                print("\n" + terminal_message)
                input("\nBotu kapatmak için Enter'a basın...")
                break
            else:
                if details:  # Hata mesajı varsa
                    logger.error("Hata oluştu!")
                    for detail in details:
                        logger.error(detail)
                    error_count += 1
                    
                    if error_count >= max_errors:
                        message = f"⚠️ Bot {error_count} kere hata aldı. 5 dakika beklenecek..."
                        logger.warning(message)
                        send_telegram_message(message)
                        time.sleep(300)
                        error_count = 0
                else:
                    logger.info(f"{TerminalColors.RED}❌ Randevu bulunamadı{TerminalColors.RESET}")
                    error_count = 0
            
            if check_type == '2':  # Belirli aralıklarla kontrol
                next_check = datetime.now() + timedelta(seconds=interval)
                logger.info(f"Bir sonraki kontrol: {next_check.strftime('%H:%M:%S')}")
                time.sleep(interval)
            else:  # Sürekli kontrol
                time.sleep(1)  # 1 saniye bekle
            
    except KeyboardInterrupt:
        logger.info("\nBot durduruldu.")
        logger.info("İyi günler!")

if __name__ == "__main__":
    main() 