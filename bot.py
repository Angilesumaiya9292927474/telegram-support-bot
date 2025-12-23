import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ============ LOGGING ============
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ CONFIG ============
BOT_TOKEN = os.environ.get("BOT_TOKEN")   # Railway Variables থেকে নেবে
ADMINS = {6187018016}

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in Railway Variables!")

users = set()
blocked_users = set()

# ============ COMMANDS ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)
    if user.id in blocked_users:
        return
    await update.message.reply_text(
        "👋 Welcome to Support Bot\n\n"
        "📩 /contact - Admin কে মেসেজ পাঠাও\n"
        "👑 /admin - Admin panel"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact_mode"] = True
    await update.message.reply_text("✍️ তোমার মেসেজ লিখো:")

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if context.user_data.get("contact_mode"):
        for admin in ADMINS:
            await context.bot.send_message(
                admin,
                f"📩 New Message\n\n"
                f"Name: {user.first_name}\n"
                f"ID: {user.id}\n\n"
                f"{update.message.text}"
            )
        await update.message.reply_text("✅ Message admin এর কাছে পাঠানো হয়েছে")
        context.user_data["contact_mode"] = False

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await update.message.reply_text(
        f"👑 Admin Panel\n\n"
        f"👥 Total Users: {len(users)}\n\n"
        f"/broadcast <msg>\n"
        f"/block <user_id>\n"
        f"/unblock <user_id>"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    msg = " ".join(context.args)
    sent = 0
    for u in users:
        if u not in blocked_users:
            try:
                await context.bot.send_message(u, msg)
                sent += 1
            except:
                pass
    await update.message.reply_text(f"Sent to {sent} users")

async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    blocked_users.add(int(context.args[0]))
    await update.message.reply_text("🚫 User blocked")

async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    blocked_users.discard(int(context.args[0]))
    await update.message.reply_text("✅ User unblocked")

# ============ MAIN ============
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("block", block_user))
    app.add_handler(CommandHandler("unblock", unblock_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))

    app.run_polling()

if __name__ == "__main__":
    main()
