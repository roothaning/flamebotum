
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Admin kullanıcılar listesi
admin_user_ids = [5630665026, 7074730627]

def admin_panel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in admin_user_ids:
        update.message.reply_text(
            "Admin Paneline Hoşgeldiniz! Aşağıdaki komutları kullanabilirsiniz:
"
            "/manageusers - Kullanıcıları yönet
"
            "/sendbonus - Bonus gönder
"
            "/withdrawals - Çekim taleplerini yönet
"
            "/referrals - Davet programını yönet"
        )
    else:
        update.message.reply_text("Bu komutu kullanma yetkiniz yok.")

def manage_users(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in admin_user_ids:
        # Kullanıcıları veritabanından veya statik bir listeden alabilirsiniz
        users = ['user1', 'user2', 'user3']
        user_list = "
".join(users)
        update.message.reply_text(f"Kayıtlı Kullanıcılar:
{user_list}")
    else:
        update.message.reply_text("Bu komutu kullanma yetkiniz yok.")

def send_bonus(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in admin_user_ids:
        if len(context.args) > 1:
            username = context.args[0]
            amount = context.args[1]
            # Bonus verme işlemi burada yapılabilir
            update.message.reply_text(f"{username} adlı kullanıcıya {amount} bonus gönderildi.")
        else:
            update.message.reply_text("Lütfen bonus miktarını ve kullanıcı adını belirtin.")
    else:
        update.message.reply_text("Bu komutu kullanma yetkiniz yok.")

def withdrawals(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in admin_user_ids:
        # Çekim taleplerini buradan kontrol edebilirsiniz
        # Örnek olarak bir liste gösterelim:
        requests = ['User1: 1000 Flame', 'User2: 500 Flame']
        request_list = "
".join(requests)
        update.message.reply_text(f"Çekim Talepleri:
{request_list}")
    else:
        update.message.reply_text("Bu komutu kullanma yetkiniz yok.")

def main():
    updater = Updater('7171119770:AAEVH-F5dJuZfSU69qGcZQNPUe0NGSEUamQ', use_context=True)
    dp = updater.dispatcher

    # Komutları ekleyelim
    dp.add_handler(CommandHandler('adminpanel', admin_panel))
    dp.add_handler(CommandHandler('manageusers', manage_users))
    dp.add_handler(CommandHandler('sendbonus', send_bonus))
    dp.add_handler(CommandHandler('withdrawals', withdrawals))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
