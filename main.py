import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers import (
    start, mining, balance, shop, buy_callback,
    daily, referral, leaderboard, handle_message
)
from clan_manager import ClanManager, button_handler  # Klan işlemleri için

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Hata mesajlarını loglar ve kullanıcıya bilgi verir."""
    logger.error(f"Hata oluştu: {context.error}")
    if update and update.message:
        await update.message.reply_text("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

async def klan_komutlari(update: Update, context):
    """Klan menüsünü gösterir."""
    keyboard = [
        [InlineKeyboardButton("Klan Kur", callback_data="create_clan")],
        [InlineKeyboardButton("Klanları Listele", callback_data="list_clans")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔹 Klan Menüsü:", reply_markup=reply_markup)

async def list_clans(update: Update, context):
    """Mevcut klanları listeleme."""
    clan_manager = ClanManager()
    clans = clan_manager.clans
    if clans:
        clan_list = "\n".join([f"📢 {clan_name} (Sahip: {clan_info['owner']}, Üye Sayısı: {len(clan_info['members'])})" for clan_name, clan_info in clans.items()])
    else:
        clan_list = "Henüz hiç klan yok."
    
    keyboard = [
        [InlineKeyboardButton("Klan Kur", callback_data="create_clan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Mevcut Klanlar:\n{clan_list}\n\nYapmak istediğiniz işlemi seçin:", reply_markup=reply_markup)

async def create_clan(update: Update, context):
    """Klan kurma işlemi."""
    await update.message.reply_text("Klan adını girin:")
    
    # Klan adı bekleniyor
    return "WAITING_FOR_CLAN_NAME"

async def handle_clan_name(update: Update, context):
    """Kullanıcıdan klan adı alındığında klan oluşturulur."""
    user_id = str(update.effective_user.id)
    clan_name = update.message.text.strip()

    clan_manager = ClanManager()
    if clan_manager.create_clan(clan_name, user_id):
        await update.message.reply_text(f"Klanınız başarıyla kuruldu: {clan_name}")
    else:
        await update.message.reply_text(f"{clan_name} zaten mevcut. Başka bir isim deneyin.")

def run_bot():
    """Botu başlatan ana fonksiyon."""
    application = Application.builder().token(TOKEN).build()

    # Komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mining", mining))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("referral", referral))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("klan", klan_komutlari))  # Klan komutu eklendi

    # Klan adı beklerken
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_clan_name))

    # Callback Query Handler (Düğmeler için)
    application.add_handler(CallbackQueryHandler(buy_callback, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(button_handler))  # Klan butonları için

    # Hata yakalama
    application.add_error_handler(error_handler)

    # Botu çalıştır
    logger.info("🔥 Flame Mining Bot Başlatılıyor...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot kullanıcı tarafından durduruldu.")
    except Exception as e:
        logger.error(f"Kritik hata: {e}")

