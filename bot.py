import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ===== CONFIG =====
BOT_TOKEN = "7985647210:AAE-qLc8cwgOJOjtzmVpAIhU9I9Clc63TXo"

ADMINS = {6187018016}

users = set()
blocked_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    if user.id in blocked_users:
        return

    await update.message.reply_text(
        f"👋 Hello {user.first_name}\n\n"
        "🤖 This is a Support Bot\n"
        "📩 Use /contact to message admin\n"
        "ℹ️ Use /help for commands"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/contact - Contact admin\n"
        "/admin - Admin panel"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Send your message for admin:")
    context.user_data["contact_mode"] = True

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    if context.user_data.get("contact_mode"):
        for admin in ADMINS:
            await context.bot.send_message(
                admin,
                f"📩 New Message\n\n👤 {user.first_name}\n🆔 {user.id}\n💬 {update.message.text}"
            )
        await update.message.reply_text("✅ Message sent to admin.")
        context.user_data["contact_mode"] = False

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await update.message.reply_text(
        f"👑 Admin Panel\n\nUsers: {len(users)}\n\n"
        "/broadcast <msg>\n/block <id>\n/unblock <id>"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    msg = " ".join(context.args)
    for u in users:
        if u not in blocked_users:
            try:
                await context.bot.send_message(u, msg)
            except:
                pass

async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = int(context.args[0])
    blocked_users.add(uid)
    await update.message.reply_text("🚫 Blocked")

async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = int(context.args[0])
    blocked_users.discard(uid)
    await update.message.reply_text("✅ Unblocked")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("block", block_user))
    app.add_handler(CommandHandler("unblock", unblock_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))

    app.run_polling()

if __name__ == "__main__":
    main()
