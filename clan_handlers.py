from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

class ClanManager:
    def __init__(self):
        # Load clans from file or database
        self.clans = {
            "ClanA": {"owner": "user123", "members": ["user123"]},
            "ClanB": {"owner": "user456", "members": ["user456"]}
        }

    def user_has_clan(self, user_id):
        for clan in self.clans.values():
            if user_id in clan['members']:
                return True
        return False

    def save_clans(self):
        # Save clans to file or database
        pass


def join_clan(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    clan_name = query.data.replace("join_", "")

    clan_manager = ClanManager()
    if clan_manager.user_has_clan(user_id):
        query.answer("Zaten bir klanda bulunuyorsunuz!")
        return

    if clan_name in clan_manager.clans:
        clan_manager.clans[clan_name]['members'].append(user_id)
        clan_manager.save_clans()
        query.answer("Klana başarıyla katıldınız!")
        show_clan_info(query, clan_name, clan_manager.clans[clan_name])
    else:
        query.answer("Klan bulunamadı!")

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

    clan_manager = ClanManager() # Added ClanManager instance here

    if user_id in clan['members']:
        keyboard.append([InlineKeyboardButton("Klandan Çık", callback_data=f"leave_{clan_name}")]) #Added clan name to callback data
    elif not clan_manager.user_has_clan(user_id):
        keyboard.append([InlineKeyboardButton("Klana Katıl", callback_data=f"join_{clan_name}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update, Update):
        update.message.reply_text(info, reply_markup=reply_markup)
    else:
        update.edit_message_text(text=info, reply_markup=reply_markup)


def leave_clan(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    clan_name = query.data.replace("leave_", "")

    clan_manager = ClanManager()
    if clan_name in clan_manager.clans:
        if user_id in clan_manager.clans[clan_name]['members']:
            clan_manager.clans[clan_name]['members'].remove(user_id)
            clan_manager.save_clans()
            query.answer("Klandan başarıyla çıktınız!")
            show_clan_info(query, clan_name, clan_manager.clans[clan_name])
        else:
            query.answer("Bu klana üye değilsiniz!")
    else:
        query.answer("Klan bulunamadı!")



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


#Example usage (needs a telegram bot setup)
#dispatcher.add_handler(CallbackQueryHandler(button_handler))