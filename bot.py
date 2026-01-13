import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")  # Set this in Render ENV
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your Telegram numeric ID

# ---------- KEYBOARDS ----------

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["💰 Purchase Subscription", "📄 My Subscriptions"],
        ["🆘 Contact Support", "🔄 Refresh Menu"],
    ],
    resize_keyboard=True,
)

PLANS_MENU = ReplyKeyboardMarkup(
    [
        ["Basic - ₹500"],
        ["Premium Plus - ₹5000"],
        ["Private Reels - ₹2000"],
        ["Premium Content VIP Users - ₹1000"],
        ["❌ Cancel"],
    ],
    resize_keyboard=True,
)

PAYMENT_MENU = ReplyKeyboardMarkup(
    [
        ["🇮🇳 Indian UPI Payment"],
        ["🌍 International Payment (Remitly)"],
        ["❌ Cancel"],
    ],
    resize_keyboard=True,
)

# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! You have been registered.\n\nMain Menu:",
        reply_markup=MAIN_MENU,
    )

# ---------- TEXT HANDLER ----------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Purchase Subscription":
        await update.message.reply_text(
            "Available subscription plans:",
            reply_markup=PLANS_MENU,
        )

    elif text == "Basic - ₹500":
        context.user_data["plan"] = "Basic - ₹500"
        await update.message.reply_text(
            """
Basic:
- Daily uploads of 2–3 pics/videos (exposure content only)
- ✅ Free demo available for this plan only

⚠️ Important Notes:
❌ No real meetings / video calls
❌ No free demos (except Plan 1)
⏳ Lifetime validity
""",
        )
        await update.message.reply_text(
            "Please select your payment method for Basic (₹500):",
            reply_markup=PAYMENT_MENU,
        )

    elif text == "🇮🇳 Indian UPI Payment":
        await update.message.reply_photo(
            photo="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=paytm.s1axuq5@pty",
            caption=(
                "💳 Please send ₹500 to VPA:\n"
                "`paytm.s1axuq5@pty`\n\n"
                "📸 After payment, send the receipt screenshot here."
            ),
            parse_mode="Markdown",
        )

    elif text == "🌍 International Payment (Remitly)":
        await update.message.reply_text(
            """
🌍 International Payment Instructions (Remitly)

1️⃣ Open or download the Remitly app  
2️⃣ Send payment using Remitly  
3️⃣ After payment, send the receipt screenshot here  
""",
        )

    elif text == "🆘 Contact Support":
        await update.message.reply_text(
            "Support will contact you shortly.\nPlease wait.",
        )

    elif text == "🔄 Refresh Menu":
        await update.message.reply_text("Main Menu:", reply_markup=MAIN_MENU)

    elif text == "❌ Cancel":
        await update.message.reply_text("Cancelled.", reply_markup=MAIN_MENU)

    else:
        await update.message.reply_text(
            "Please use the menu buttons.",
            reply_markup=MAIN_MENU,
        )

# ---------- PHOTO HANDLER ----------

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📸 Payment screenshot received from user @{update.effective_user.username}",
    )

    await update.message.reply_text(
        "📩 Screenshot received.\nPlease wait for admin approval.",
    )

# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
