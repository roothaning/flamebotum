async def leave_clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if db.leave_clan(user_id):
        await update.message.reply_text("Klandan başarıyla ayrıldınız.")
    else:
        await update.message.reply_text("Klandan ayrılamadınız. Klan lideri olabilirsiniz.")

async def view_clan_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clan_members = db.get_clan_members(user_id)
    if clan_members:
        message = "Klan Üyeleri:\n" + "\n".join(clan_members)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Klan üyeleri alınamadı veya bir klana üye değilsiniz.")