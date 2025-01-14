import requests
import time
from datetime import datetime, timedelta
import platform
import os
from bs4 import BeautifulSoup

# URL'ler
VISA_URLS = {
    'italy': {
        'base': 'https://www.idata.com.tr/ita/tr',
        'ankara': 'https://www.idata.com.tr/ita/tr/ankara-randevu',  # iData Ankara randevu sayfası
        'istanbul': 'https://www.idata.com.tr/ita/tr/istanbul-randevu'  # iData İstanbul randevu sayfası
    },
    'spain': {
        'base': 'https://turkey.blsspainvisa.com',
        'ankara': 'https://turkey.blsspainvisa.com/appointment/slots',  # BLS Ankara randevu sayfası
        'istanbul': 'https://turkey.blsspainvisa.com/appointment/slots'  # BLS İstanbul randevu sayfası
    }
}

def play_notification_sound():
    """Sistem sesli uyarı çal ve sürekli çal"""
    while True:  # Sürekli ses çal (kullanıcı fark edene kadar)
        if platform.system() == 'Darwin':  # macOS
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif platform.system() == 'Windows':
            import winsound
            winsound.Beep(1000, 1000)
        else:  # Linux
            os.system('beep')
        time.sleep(1)  # 1 saniye bekle ve tekrar çal

def extract_appointment_details(html, country):
    """En yakın randevu tarihini bul (Turist vizesi için)"""
    soup = BeautifulSoup(html, 'html.parser')
    
    if country == 'italy':
        # iData sitesi için randevu tarihi kontrolü (Turist vizesi)
        dates = []
        available_dates = soup.find_all(['div', 'span', 'a'], string=lambda text: text and any(month in text.lower() for month in ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']))
        
        for date in available_dates:
            date_text = date.get_text(strip=True)
            if date_text and not any(x in date_text.lower() for x in ['randevu bulunmamaktadır', 'no appointment', 'closed']):
                if 'turist' in date_text.lower() or 'tourist' in date_text.lower() or 'c tipi' in date_text.lower():
                    dates.append(date_text)
        
        if dates:
            return [f"En yakın turist vizesi randevu tarihi: {dates[0]}"]
    
    elif country == 'spain':
        # BLS sitesi için randevu tarihi kontrolü (Turist vizesi)
        dates = []
        available_slots = soup.find_all(['div', 'span', 'a'], string=lambda text: text and any(month in text.lower() for month in ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']))
        
        for slot in available_slots:
            slot_text = slot.get_text(strip=True)
            if slot_text and not any(x in slot_text.lower() for x in ['no slots', 'no appointment', 'closed']):
                if 'turist' in slot_text.lower() or 'tourist' in slot_text.lower() or 'short stay' in slot_text.lower():
                    dates.append(slot_text)
        
        if dates:
            return [f"En yakın turist vizesi randevu tarihi: {dates[0]}"]
    
    return ["Turist vizesi için randevu var! Lütfen hemen siteyi kontrol edin."]

def check_appointment(country, city):
    """Randevu kontrolü yap (Turist vizesi için)"""
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
        print(f"\nBağlanılıyor: {url}")  # URL'yi göster
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Durum Kodu: {response.status_code}")  # HTTP durum kodunu göster
        
        html = response.text
        html_lower = html.lower()
        
        # İtalya için kontrol
        if country == 'italy':
            # iData sistemi için özel kontrol
            if 'randevu bulunmamaktadır' not in html_lower and 'no appointment available' not in html_lower:
                if 'turist' in html_lower or 'tourist' in html_lower or 'c tipi' in html_lower or 'schengen' in html_lower:
                    details = extract_appointment_details(html, country)
                    return True, details
        
        # İspanya için kontrol
        elif country == 'spain':
            # BLS sistemi için özel kontrol
            if 'no slots available' not in html_lower and 'no appointment available' not in html_lower:
                if 'turist' in html_lower or 'tourist' in html_lower or 'short stay' in html_lower or 'schengen' in html_lower:
                    details = extract_appointment_details(html, country)
                    return True, details
        
        return False, []
        
    except requests.exceptions.ConnectionError:
        print(f"\nBağlantı hatası: {url}")  # Hata durumunda URL'yi göster
        return False, ["Site bağlantısı başarısız oldu. İnternet bağlantınızı kontrol edin."]
    except requests.exceptions.Timeout:
        print(f"\nTimeout hatası: {url}")  # Timeout durumunda URL'yi göster
        return False, ["Site yanıt vermiyor (timeout). Daha sonra tekrar deneyin."]
    except Exception as e:
        print(f"\nBeklenmeyen hata: {str(e)}")  # Hatayı detaylı göster
        return False, [f"Beklenmeyen bir hata oluştu: {str(e)}"]

def main():
    # Kullanıcı girişi
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
    
    # Kontrol sıklığı
    interval = int(input("\nKontrol sıklığı (dakika): "))
    interval = max(1, interval)  # En az 1 dakika
    
    print(f"\n{country.upper()} - {city.upper()} için turist vizesi randevu kontrolü başlıyor...")
    print(f"Bot her {interval} dakikada bir kontrol yapacak")
    print("Botu durdurmak için Ctrl+C tuşlarına basın\n")
    
    error_count = 0  # Hata sayacı
    max_errors = 3   # Maximum hata sayısı
    
    try:
        while True:  # Sonsuz döngü - gerçek bir bot gibi
            now = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{now}] Kontrol ediliyor...")  # Yeni satırda başlat
            
            has_appointment, details = check_appointment(country, city)
            if has_appointment:
                print("\n🔔 RANDEVU BULUNDU! 🎉")  # Daha görünür bildirim
                
                # Yeni thread'de sürekli ses çal
                import threading
                sound_thread = threading.Thread(target=play_notification_sound)
                sound_thread.daemon = True
                sound_thread.start()
                
                print(f"\n{country.upper()} - {city.upper()} için turist vizesi randevusu bulundu!")
                print("\nBilgi:")
                for detail in details:
                    print(f"- {detail}")
                print(f"\nSite adresi: {VISA_URLS[country][city]}")
                print("\nLütfen hemen siteye giriş yapın ve randevuyu alın!")
                
                input("\nBildirimi durdurup botu kapatmak için Enter'a basın...")
                break
            else:
                if details:  # Hata mesajı varsa
                    print("❌ Hata!")
                    for detail in details:
                        print(f"- {detail}")
                    error_count += 1
                    
                    if error_count >= max_errors:
                        print(f"\n⚠️ Çok fazla hata oluştu ({error_count} kere). 5 dakika bekleyip tekrar deneyelim...")
                        time.sleep(300)  # 5 dakika bekle
                        error_count = 0
                else:
                    print("❌ Randevu bulunamadı")
                    error_count = 0
            
            # Bir sonraki kontrole kadar bekle
            next_check = datetime.now() + timedelta(minutes=interval)
            print(f"\nBir sonraki kontrol: {next_check.strftime('%H:%M:%S')}")
            time.sleep(interval * 60)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Bot durduruldu.")
        print("İyi günler!")

if __name__ == "__main__":
    main() 