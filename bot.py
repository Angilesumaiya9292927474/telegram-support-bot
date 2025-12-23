from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

BOT_TOKEN = os.getenv("7985647210:AAHmkdyOVxKeaQjm077d5tEr6USjp_IuPtM")
ADMINS = [6187018016]

users = set()
blocked = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text("🤖 Bot is running!")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await update.message.reply_text(
        "👑 Admin Panel\n"
        f"👥 Total Users: {len(users)}\n\n"
        "/broadcast <msg>\n"
        "/block <user_id>\n"
        "/unblock <user_id>"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    msg = " ".join(context.args)
    for u in users:
        if u not in blocked:
            try:
                await context.bot.send_message(u, msg)
            except:
                pass

async def block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    blocked.add(int(context.args[0]))
    await update.message.reply_text("User blocked")

async def unblock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    blocked.discard(int(context.args[0]))
    await update.message.reply_text("User unblocked")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("block", block))
    app.add_handler(CommandHandler("unblock", unblock))

    app.run_polling()

if __name__ == "__main__":
    main()
