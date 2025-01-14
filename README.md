# Schengen Vize Randevu Kontrol Botu

Bu bot, İtalya ve İspanya Schengen vizesi için randevu kontrolü yapar. Bot özellikle turist vizesi randevularını kontrol eder.

## Özellikler

- İtalya (iData) ve İspanya (BLS) vize sistemlerini kontrol eder
- Ankara ve İstanbul şehirleri için randevu kontrolü yapar
- Sesli ve görsel bildirimler
- Otomatik hata yönetimi ve yeniden deneme
- Özelleştirilebilir kontrol sıklığı

## Gereksinimler

```bash
Python 3.x
requests
beautifulsoup4
```

## Kurulum

1. Repo'yu klonlayın:
```bash
git clone https://github.com/KULLANICI_ADI/schengen-visa-appointment-bot.git
cd schengen-visa-appointment-bot
```

2. Virtual environment oluşturun:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
.\venv\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Botu çalıştırın:
```bash
python3 check_appointment.py
```

2. İstenilen bilgileri girin:
   - Ülke seçin (İtalya/İspanya)
   - Şehir seçin (Ankara/İstanbul)
   - Kontrol sıklığını dakika olarak girin

3. Bot çalışmaya başlayacak ve randevu bulduğunda sizi bilgilendirecektir.

## Notlar

- Bot randevu bulduğunda sesli uyarı verecektir
- Ctrl+C ile botu durdurabilirsiniz
- Çok fazla hata alındığında bot otomatik olarak 5 dakika bekleyecektir

## Lisans

MIT License 