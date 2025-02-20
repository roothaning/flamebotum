from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime
from database import Database
from utils import can_mine, calculate_mining_reward, can_claim_daily, format_time_until_next_mining
from config import DAILY_BONUS, REFERRAL_BONUS, EQUIPMENT

db = Database()

# Ana menü butonları
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("⛏️ Mining"), KeyboardButton("💰 Bakiye")],
    [KeyboardButton("🏪 Mağaza"), KeyboardButton("🎁 Günlük Bonus")],
    [KeyboardButton("👥 Referans"), KeyboardButton("🏆 Sıralama")]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db.get_user(user_id)  # Initialize user if not exists

    # Check for referral
    if len(context.args) > 0:
        try:
            referrer_id = int(context.args[0])
            if db.add_referral(user_id, referrer_id):
                db.add_coins(referrer_id, REFERRAL_BONUS)
                db.add_coins(user_id, REFERRAL_BONUS)
                await update.message.reply_text(f"🎉 Referans bonusu kazandınız: {REFERRAL_BONUS} coin!")
        except ValueError:
            pass

    welcome_text = """🔥 Flame Coin Bot'a Hoş Geldin! 🔥

Madenciliğe başlamak için aşağıdaki butonları kullanabilirsin!

Özellikler:
⛏️ Mining - Flame Coin madenciliği yap
💰 Bakiye - Bakiyeni kontrol et
🏪 Mağaza - Ekipman mağazası
🎁 Günlük Bonus - Günlük bonus al
👥 Referans - Referans linkini al
🏆 Sıralama - Global sıralama"""

    await update.message.reply_text(welcome_text, reply_markup=MAIN_MENU_KEYBOARD)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "⛏️ Mining":
        await mining(update, context)
    elif text == "💰 Bakiye":
        await balance(update, context)
    elif text == "🏪 Mağaza":
        await shop(update, context)
    elif text == "🎁 Günlük Bonus":
        await daily(update, context)
    elif text == "👥 Referans":
        await referral(update, context)
    elif text == "🏆 Sıralama":
        await leaderboard(update, context)

async def mining(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)

    if not can_mine(user['last_mining']):
        next_mining = format_time_until_next_mining(user['last_mining'])
        await update.message.reply_text(f"⏳ Sonraki madencilik için bekleyin: {next_mining}", reply_markup=MAIN_MENU_KEYBOARD)
        return

    reward = calculate_mining_reward(user['equipment'])
    new_balance = db.add_coins(user_id, reward)
    user['last_mining'] = datetime.now().isoformat()
    db.update_user(user_id, user)

    await update.message.reply_text(
        f"⛏️ Madencilik başarılı!\n💰 Kazanılan: {reward} coin\n💎 Yeni bakiye: {new_balance} coin",
        reply_markup=MAIN_MENU_KEYBOARD
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    equipment_text = "\n".join([f"- {item}" for item in user['equipment']]) if user['equipment'] else "Yok"

    await update.message.reply_text(
        f"💰 Bakiye: {user['coins']} coin\n\n🛠️ Ekipmanlar:\n{equipment_text}",
        reply_markup=MAIN_MENU_KEYBOARD
    )

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for item, details in EQUIPMENT.items():
        keyboard.append([InlineKeyboardButton(
            f"{item.title()} - {details['cost']} coin (+ {details['mining_bonus']} bonus)",
            callback_data=f"buy_{item}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏪 Mağaza - Ekipman Listesi:", reply_markup=reply_markup)

async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    item = query.data.split('_')[1]

    await query.answer()

    if item not in EQUIPMENT:
        await query.message.reply_text("❌ Geçersiz ekipman!", reply_markup=MAIN_MENU_KEYBOARD)
        return

    user = db.get_user(user_id)
    cost = EQUIPMENT[item]['cost']

    if item in user['equipment']:
        await query.message.reply_text("❌ Bu ekipmana zaten sahipsin!", reply_markup=MAIN_MENU_KEYBOARD)
        return

    if user['coins'] < cost:
        await query.message.reply_text(
            f"❌ Yeterli coin yok! Gereken: {cost} coin, Mevcut: {user['coins']} coin",
            reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    db.remove_coins(user_id, cost)
    db.add_equipment(user_id, item)
    equipment_text = "\n".join([f"- {eq}" for eq in user['equipment'] + [item]])

    await query.message.edit_text(
        f"✅ {item.title()} başarıyla satın alındı!\n\n🛠️ Ekipmanlarınız:\n{equipment_text}",
        reply_markup=MAIN_MENU_KEYBOARD
    )

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)

    if not can_claim_daily(user['last_daily']):
        await update.message.reply_text(
            "❌ Günlük bonusu zaten aldınız! Yarın tekrar gelin.",
            reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    new_balance = db.add_coins(user_id, DAILY_BONUS)
    user['last_daily'] = datetime.now().isoformat()
    db.update_user(user_id, user)

    await update.message.reply_text(
        f"🎁 Günlük bonus alındı: +{DAILY_BONUS} coin\n💰 Yeni bakiye: {new_balance} coin",
        reply_markup=MAIN_MENU_KEYBOARD
    )

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = await context.bot.get_me()
    bot_username = bot.username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    user = db.get_user(user_id)
    referral_count = len(user['referrals'])
    earned_coins = referral_count * REFERRAL_BONUS

    await update.message.reply_text(
        f"👥 Referans Sistemi\n\n"
        f"🔗 Referans linkiniz:\n{referral_link}\n\n"
        f"📊 Toplam referans: {referral_count}\n"
        f"💰 Kazanılan toplam: {earned_coins} coin\n"
        f"💎 Referans başına: {REFERRAL_BONUS} coin",
        reply_markup=MAIN_MENU_KEYBOARD
    )

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_miners = db.get_top_miners(10)  # En iyi 10 madenci

    if not top_miners:
        await update.message.reply_text(
            "Henüz sıralama oluşturulmadı!",
            reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    message = "🏆 En İyi Madenciler 🏆\n\n"
    for index, (user_id, data) in enumerate(top_miners, 1):
        message += f"{index}. ID: {user_id} - {data['coins']} coin\n"

    await update.message.reply_text(message, reply_markup=MAIN_MENU_KEYBOARD)