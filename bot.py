import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7985647210:AAE-qLc8cwgOJOjtzmVpAIhU9I9Clc63TXo"
ADMINS = {6187018016}

users = set()

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text("👋 Welcome to Support Bot\nUse /contact to send message")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = True
    await update.message.reply_text("✍️ Send your message:")

async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("contact"):
        for admin in ADMINS:
            await context.bot.send_message(
                admin,
                f"📩 New Message\n\nName: {update.effective_user.first_name}\nID: {update.effective_user.id}\n\n{update.message.text}"
            )
        await update.message.reply_text("✅ Sent to admin")
        context.user_data["contact"] = False

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await update.message.reply_text(f"👑 Admin Panel\nTotal Users: {len(users)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
