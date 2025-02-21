import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers import (
    start, mining, balance, shop, buy_callback,
    daily, referral, leaderboard, handle_message
)
from handlers.clan_manager import button_handler  # Klan işlemleri için

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

    # Mesaj handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

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
