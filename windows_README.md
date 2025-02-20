# Flame Coin Bot - Windows Kurulum Rehberi

## Gereksinimler
1. Python 3.11.7 (https://www.python.org/downloads/)
2. Telegram Bot Token (@BotFather üzerinden alınmalı)

## Kurulum Adımları

1. Python'u indirin ve yükleyin:
   - https://www.python.org/downloads/release/python-3117/ adresinden "Windows installer (64-bit)" sürümünü indirin
   - İndirilen dosyayı çalıştırın
   - Kurulum sırasında "Add Python 3.11 to PATH" seçeneğini işaretleyin
   - "Install Now" ile kurulumu tamamlayın

2. Proje dosyalarını çıkartın:
   - İndirdiğiniz zip dosyasını bir klasöre çıkartın (örn: C:\FlameCoinBot)

3. Gerekli kütüphaneleri yükleyin:
   - Komut istemini (cmd) yönetici olarak çalıştırın
   - Proje klasörüne gidin: `cd C:\FlameCoinBot`
   - Şu komutu çalıştırın: `pip install python-telegram-bot==20.7 python-dotenv`

4. Bot token'ını ayarlayın:
   - Proje klasöründe `.env` isimli bir dosya oluşturun
   - İçine şunu yazın: `TELEGRAM_BOT_TOKEN=your_token_here`
   - "your_token_here" yerine @BotFather'dan aldığınız token'ı yazın

5. Botu çalıştırın:
   - Komut isteminde proje klasöründeyken: `python main.py`
   - Bot başarıyla çalıştığında konsolda "Bot starting..." mesajını göreceksiniz

## Bot Özellikleri
- ⛏️ Mining - Flame Coin madenciliği
- 💰 Bakiye kontrolü
- 🏪 Ekipman mağazası
- 🎁 Günlük bonus
- 👥 Referans sistemi
- 🏆 Global sıralama

## Sorun Giderme
1. "python was not found" hatası:
   - Python'u yeniden yükleyin ve "Add Python to PATH" seçeneğini işaretlediğinizden emin olun

2. "ModuleNotFoundError" hatası:
   - Komut istemini yönetici olarak çalıştırıp kütüphaneleri yeniden yükleyin:
   ```
   pip install python-telegram-bot==20.7 python-dotenv
   ```

3. Bot çalışmıyor:
   - .env dosyasındaki token'ın doğru olduğundan emin olun
   - Telegram'da botunuzu başlatmak için /start komutunu kullanın
4. Güncelleyerek Düzeltme
Eski API'yi kullanıyorsan ve uyumsuzluk varsa, yeni API'ye geçmelisin. Ama önce paketi güncellemek sorunu çözüyor mu bakalım:

pip install --upgrade python-telegram-bot

Eğer proje eski API'yi gerektiriyorsa, v13 gibi eski bir sürümü yükleyerek çalıştırabilirsin:

pip install python-telegram-bot==13.15
## İletişim
Sorunlarınız için: [İletişim bilgileriniz]
