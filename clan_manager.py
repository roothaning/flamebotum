from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton

class ClanManager:
    def __init__(self):
        self.clans = {
            "ClanA": {"owner": "user123", "members": ["user123"]},
            "ClanB": {"owner": "user456", "members": ["user456"]},
        }

    def user_has_clan(self, user_id):
        for clan in self.clans.values():
            if user_id in clan['members']:
                return True
        return False

    def create_clan(self, clan_name, owner_id):
        if clan_name in self.clans:
            return False  # Klan zaten var
        self.clans[clan_name] = {"owner": owner_id, "members": [owner_id]}
        return True

    def save_clans(self):
        # Veritabanı veya dosyaya kaydedilebilir
        pass

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    clan_manager = ClanManager()

    if query.data.startswith("leave_"):
        leave_clan(update, context)
    elif query.data.startswith("view_"):
        clan_name = query.data.replace("view_", "")
        if clan_name in clan_manager.clans:
            show_clan_info(query, clan_name, clan_manager.clans[clan_name])
    elif query.data.startswith("join_"):
        join_clan(update, context)

def show_clan_info(update, clan_name, clan):
    members_count = len(clan['members'])
    info = f"📢 Klan: {clan_name}\n"
    info += f"👑 Sahip: {clan['owner']}\n"
    info += f"👥 Üye Sayısı: {members_count}"

    keyboard = []
    if isinstance(update, Update):
        user_id = str(update.effective_user.id)
    else:
        user_id = str(update.from_user.id)

    if user_id in clan['members']:
        keyboard.append([InlineKeyboardButton("Klandan Çık", callback_data=f"leave_{clan_name}")])
    elif not ClanManager().user_has_clan(user_id):
        keyboard.append([InlineKeyboardButton("Klana Katıl", callback_data=f"join_{clan_name}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update, Update):
        update.message.reply_text(info, reply_markup=reply_markup)
    else:
        update.edit_message_text(text=info, reply_markup=reply_markup)
