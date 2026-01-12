import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")       # Set this in Render
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your Telegram user ID


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Send Screenshot"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome!\n\nPlease send your screenshot for verification.",
        reply_markup=reply_markup
    )


# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    caption = (
        f"📩 *New Message*\n\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 ID: `{user.id}`\n\n"
        f"💬 Message:\n{text}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=caption,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ Message received.\nPlease wait for admin approval."
    )


# Handle photo uploads
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]

    caption = (
        f"📸 *New Screenshot*\n\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 ID: `{user.id}`"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "📸 Screenshot received.\nPlease wait for admin approval."
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
