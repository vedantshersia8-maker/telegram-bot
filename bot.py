import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# CONFIG
# =====================
TOKEN = os.getenv("BOT_TOKEN")   # set in Render Environment
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # replace OR set env

# temporary memory (for now)
user_plan = {}

# =====================
# MENUS
# =====================
def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["💰 Purchase Subscription", "📄 My Subscriptions"],
            ["🆘 Contact Support", "🔄 Refresh Menu"]
        ],
        resize_keyboard=True
    )

def plans_menu():
    return ReplyKeyboardMarkup(
        [
            ["Basic - ₹500"],
            ["Premium Plus - ₹5000"],
            ["Private Reels - ₹2000"],
            ["VIP Users - ₹1000"],
            ["⬅ Back"]
        ],
        resize_keyboard=True
    )

def payment_menu():
    return ReplyKeyboardMarkup(
        [
            ["🇮🇳 Indian UPI Payment"],
            ["🌍 International Payment"],
            ["❌ Cancel"]
        ],
        resize_keyboard=True
    )

# =====================
# COMMANDS
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ You are registered!\n\nWelcome to the bot 👋",
        reply_markup=main_menu()
    )

# =====================
# TEXT HANDLER
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # ADMIN ACTIONS
    if text.startswith("✅ Approve"):
        uid = int(text.split()[-1])
        await context.bot.send_message(
            chat_id=uid,
            text="🎉 Payment approved!\nYou will be added shortly."
        )
        await update.message.reply_text("User approved ✅")
        return

    if text.startswith("❌ Reject"):
        uid = int(text.split()[-1])
        await context.bot.send_message(
            chat_id=uid,
            text="❌ Payment rejected.\nPlease contact support."
        )
        await update.message.reply_text("User rejected ❌")
        return

    # USER FLOW
    if text == "💰 Purchase Subscription":
        await update.message.reply_text(
            "Choose a plan:",
            reply_markup=plans_menu()
        )

    elif text == "🔄 Refresh Menu" or text == "⬅ Back":
        await update.message.reply_text(
            "Main Menu:",
            reply_markup=main_menu()
        )

    elif text in ["Basic - ₹500", "Premium Plus - ₹5000", "Private Reels - ₹2000", "VIP Users - ₹1000"]:
        plan, price = text.split(" - ")
        user_plan[user_id] = (plan, price)

        await update.message.reply_text(
            f"📦 *{plan}*\nPrice: {price}\n\nSelect payment method:",
            parse_mode="Markdown",
            reply_markup=payment_menu()
        )

    elif text == "🇮🇳 Indian UPI Payment":
        if user_id not in user_plan:
            await update.message.reply_text("Please select a plan first.")
            return

        await update.message.reply_text(
            "📲 *UPI Payment*\n\n"
            "UPI ID:\n"
            "`paytm.s1axuq5@pty`\n\n"
            "After payment, send screenshot here.",
            parse_mode="Markdown"
        )

    elif text == "🌍 International Payment":
        await update.message.reply_text(
            "🌍 International payments coming soon.\nContact support."
        )

    elif text == "❌ Cancel":
        await update.message.reply_text(
            "Cancelled.",
            reply_markup=main_menu()
        )

    else:
        await update.message.reply_text("Please use menu buttons.")

# =====================
# PHOTO HANDLER
# =====================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    plan = user_plan.get(user_id, ("Unknown", "Unknown"))

    caption = (
        "📸 *Payment Proof*\n\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 ID: `{user_id}`\n"
        f"📦 Plan: {plan[0]} ({plan[1]})"
    )

    keyboard = ReplyKeyboardMarkup(
        [[f"✅ Approve {user_id}", f"❌ Reject {user_id}"]],
        resize_keyboard=True
    )

    # forward photo to admin
    await update.message.forward(chat_id=ADMIN_ID)

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=caption,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    await update.message.reply_text(
        "✅ Screenshot received.\nWaiting for admin approval."
    )

# =====================
# MAIN
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
