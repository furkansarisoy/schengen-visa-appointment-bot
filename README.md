# Schengen Vize Randevu Kontrol Programı 🔍

Bu program, Schengen vizesi için randevu kontrolü yapmanızı sağlar. Program belirttiğiniz ülke ve şehir için düzenli olarak randevu kontrolü yapar ve uygun randevu bulunduğunda Telegram üzerinden bildirim gönderir.

## Özellikler ✨

- 17 Schengen ülkesi için randevu kontrolü:
  - Fransa 🇫🇷
  - Almanya 🇩🇪
  - Hollanda 🇳🇱
  - İtalya 🇮🇹
  - İspanya 🇪🇸
  - Yunanistan 🇬🇷
  - Belçika 🇧🇪
  - Avusturya 🇦🇹
  - Danimarka 🇩🇰
  - İsveç 🇸🇪
  - İsviçre 🇨🇭
  - Norveç 🇳🇴
  - Finlandiya 🇫🇮
  - Portekiz 🇵🇹
  - Çek Cumhuriyeti 🇨🇿
  - Macaristan 🇭🇺
  - Polonya 🇵🇱
- Türkiye'deki tüm VFS Global merkezleri desteklenir
- Telegram üzerinden anlık bildirimler
- Kullanıcı dostu menü arayüzü
- Otomatik randevu kontrolü
- Tarih bazlı sıralama ve Türkçe tarih formatı

## Güvenlik Uyarıları ⚠️

1. `.env` dosyası asla GitHub'a yüklenmemeli
2. Bot token'ınızı asla public yapmamalısınız
3. Eğer token'ınız yanlışlıkla public olduysa:
   - Hemen @BotFather'dan `/revoke` komutu ile iptal edin
   - Yeni bir bot token alın
   - `.env` dosyasını güncelleyin

## Kurulum 🛠️

1. Python 3.8 veya üzeri sürümü yükleyin
2. Gerekli paketleri yükleyin:
```bash
pip install python-telegram-bot python-dotenv aiohttp
```

3. Telegram Bot Kurulumu:
   1. Telegram'da [@BotFather](https://t.me/BotFather) ile yeni bir sohbet başlatın
   2. `/newbot` komutunu gönderin
   3. Bot için bir isim girin (örn: "Schengen Randevu Bot")
   4. Bot için bir kullanıcı adı girin (örn: "schengen_randevu_bot")
   5. BotFather size bir API token verecek (örn: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
   6. Bu token'ı güvenli bir yerde saklayın

4. Chat ID Alma:
   1. Oluşturduğunuz bot ile bir sohbet başlatın
   2. Bota herhangi bir mesaj gönderin
   3. Tarayıcınızda şu adrese gidin:
      ```
      https://api.telegram.org/bot<YourBOTToken>/getUpdates
      ```
      (YourBOTToken yerine BotFather'dan aldığınız token'ı yazın)
   4. Açılan sayfada "chat" altındaki "id" değerini bulun ve not alın

5. `.env` Dosyası Oluşturma:
   1. Proje klasöründe `.env` adında bir dosya oluşturun
   2. Dosyaya şu bilgileri ekleyin:
      ```
      TELEGRAM_BOT_TOKEN=your_bot_token
      TELEGRAM_CHAT_ID=your_chat_id
      ```
   3. `your_bot_token` yerine BotFather'dan aldığınız token'ı yazın
   4. `your_chat_id` yerine bir önceki adımda aldığınız Chat ID'yi yazın

6. Bot'u Test Etme:
   1. Programı çalıştırın:
      ```bash
      python check_appointment.py
      ```
   2. Randevu bulunduğunda bot size otomatik olarak bildirim gönderecektir

Not: Telegram botunuzun gizliliğini korumak için:
- `.env` dosyasını asla GitHub'a yüklemeyin
- Bot token'ınızı kimseyle paylaşmayın
- Botunuzu sadece kendi kullanımınız için ayarlayın

## Kullanım 📱

1. Programı başlatın:
```bash
python check_appointment.py
```

2. Ülke seçimi yapın (1-17):
   - Fransa 🇫🇷
   - Almanya 🇩🇪
   - Hollanda 🇳🇱
   - İtalya 🇮🇹
   - İspanya 🇪🇸
   - Yunanistan 🇬🇷
   - Belçika 🇧🇪
   - Avusturya 🇦🇹
   - Danimarka 🇩🇰
   - İsveç 🇸🇪
   - İsviçre 🇨🇭
   - Norveç 🇳��
   - Finlandiya ��🇮
   - Portekiz 🇵🇹
   - Çek Cumhuriyeti 🇨🇿
   - Macaristan 🇭🇺
   - Polonya 🇵🇱

3. Şehir seçimi yapın:
   - Ankara
   - Istanbul
   - Izmir
   - Antalya
   - Gaziantep
   - Bursa
   - Edirne

4. Kontrol sıklığını belirleyin (1-60 dakika)

## Menü Seçenekleri 📋

- **Yeni sorgu başlat**: Yeni ülke ve şehir için randevu kontrolü başlatır
- **Mevcut sorguyu durdur**: Aktif sorguyu durdurur
- **Programdan çık**: Programı sonlandırır

## Bildirimler 📬

Program randevu bulduğunda Telegram üzerinden aşağıdaki bilgileri içeren bir bildirim gönderir:
- Ülke adı (Türkçe)
- Merkez bilgisi
- Randevu tarihi (örn: 7 Şubat 2025)
- Vize kategorisi
- Alt kategori (varsa)
- Randevu linki

## Kısayollar ⌨️

- **Ctrl+C**: Menüye dönmek için
- **3**: Programdan çıkmak için

## Notlar 📝

- Program her kontrol sonrası belirlediğiniz süre kadar bekler
- Randevular tarih sırasına göre listelenir
- Telegram bildirimleri için bot token ve chat ID gereklidir
- Program kesintisiz çalışabilir, istediğiniz zaman menüden kontrol edebilirsiniz

## Hata Durumları ⚠️

Program aşağıdaki durumlarda sizi bilgilendirir:
- API bağlantı hataları
- Geçersiz ülke/şehir seçimleri
- Telegram bildirim hataları
- Diğer beklenmeyen hatalar

## Katkıda Bulunma 🤝

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/amazing`)
5. Pull Request oluşturun 