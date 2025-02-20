import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers import (
    start, mining, balance, shop, buy_callback,
    daily, referral, leaderboard, handle_message
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.error(f"Exception while handling an update: {context.error}")
    if update and update.message:
        await update.message.reply_text("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

def run_bot():
    """Start the bot."""
    # Create application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mining", mining))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("referral", referral))
    application.add_handler(CommandHandler("leaderboard", leaderboard))

    # Message handler for buttons
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback queries for shop
    application.add_handler(CallbackQueryHandler(buy_callback, pattern="^buy_"))

    # Error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")