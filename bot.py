import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("7985647210:AAHFddDaZXaKfWK9owYCrlIm3DLtOp9yWyA")
ADMIN_IDS = [8136997138]

logging.basicConfig(level=logging.INFO)

users = set()
blocked = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in blocked:
        return
    users.add(user_id)
    await update.message.reply_text("👋 Welcome to the bot!")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    await update.message.reply_text(
        f"👑 Admin Panel\n\n"
        f"👥 Total Users: {len(users)}\n\n"
        f"/broadcast <msg> - Send to all users\n"
        f"/block <user_id> - Block user\n"
        f"/unblock <user_id> - Unblock user"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    msg = " ".join(context.args)
    for u in users:
        try:
            await context.bot.send_message(chat_id=u, text=msg)
        except:
            pass

async def block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    uid = int(context.args[0])
    blocked.add(uid)
    await update.message.reply_text(f"❌ Blocked {uid}")

async def unblock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    uid = int(context.args[0])
    blocked.discard(uid)
    await update.message.reply_text(f"✅ Unblocked {uid}")

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
