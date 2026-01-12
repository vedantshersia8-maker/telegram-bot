import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8498170357

# Store user selections in memory (simple)
user_plan = {}

def main_menu(update):
    keyboard = [
        ["💰 Purchase Subscription", "📄 My Subscriptions"],
        ["🆘 Contact Support", "🔄 Refresh Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Welcome! You have been registered.\n\nMain Menu:",
        reply_markup=reply_markup
    )

def start(update, context):
    main_menu(update)

def show_plans(update):
    keyboard = [
        ["Basic - ₹500"],
        ["Premium Plus - ₹5000"],
        ["Private Reels - ₹2000"],
        ["VIP Users - ₹1000"],
        ["⬅ Back"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Available subscription plans:",
        reply_markup=reply_markup
    )

def show_payment_methods(update, plan_name, price):
    keyboard = [
        ["🇮🇳 Indian UPI Payment"],
        ["🌍 International Payment"],
        ["❌ Cancel"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Please select your payment method for:\n\n"
        f"{plan_name} ({price})",
        reply_markup=reply_markup
    )

def handle_text(update, context):
    text = update.message.text
    user_id = update.message.from_user.id
	
    if text.startswith("✅ Approve"):
        user_id = int(text.split()[-1])
        context.bot.send_message(
            chat_id=user_id,
            text="🎉 Payment approved!\nYou will be added shortly."
        )
        update.message.reply_text("User approved ✅")
        return

    if text.startswith("❌ Reject"):
        user_id = int(text.split()[-1])
        context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment rejected.\nPlease contact support."
        )
        update.message.reply_text("User rejected ❌")
        return


    if text == "💰 Purchase Subscription":
        show_plans(update)

    elif text == "🔄 Refresh Menu":
        main_menu(update)

    elif text == "⬅ Back":
        main_menu(update)

    elif text == "Basic - ₹500":
        user_plan[user_id] = ("Basic", "₹500")
        update.message.reply_text(
            "📦 *Basic Plan*\n"
            "- Daily uploads of 2–3 pics/videos\n"
            "- Free demo available\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Basic", "₹500")

    elif text == "Premium Plus - ₹5000":
        user_plan[user_id] = ("Premium Plus", "₹5000")
        update.message.reply_text(
            "📦 *Premium Plus*\n"
            "- Access to premium group\n"
            "- Daily uploads\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Premium Plus", "₹5000")

    elif text == "Private Reels - ₹2000":
        user_plan[user_id] = ("Private Reels", "₹2000")
        update.message.reply_text(
            "📦 *Private Reels*\n"
            "- Unlimited reels\n"
            "- Daily uploads\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Private Reels", "₹2000")

    elif text == "VIP Users - ₹1000":
        user_plan[user_id] = ("VIP Users", "₹1000")
        update.message.reply_text(
            "📦 *VIP Users*\n"
            "- Exclusive videos\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "VIP Users", "₹1000")

    elif text == "🇮🇳 Indian UPI Payment":
        plan = user_plan.get(user_id)
        if not plan:
            update.message.reply_text("Please select a plan first.")
            return

        update.message.reply_text(
            "📲 *UPI Payment*\n\n"
            "Send payment to:\n"
            "`paytm.s1axuq5@pty`\n\n"
            "After payment, send screenshot here.",
            parse_mode="Markdown"
        )

        # OPTIONAL: Send QR image
        # update.message.reply_photo(open("qr.png", "rb"))

    elif text == "🌍 International Payment":
        update.message.reply_text(
            "🌍 *International Payment*\n\n"
            "Payment via Remitly.\n"
            "Instructions will be shared soon.",
            parse_mode="Markdown"
        )

    elif text == "❌ Cancel":
        main_menu(update)

    else:
        update.message.reply_text("Please use the menu buttons.")
		
def handle_photo(update, context):
    user = update.message.from_user
    user_id = user.id
    plan = user_plan.get(user_id, ("Unknown", "Unknown"))

    caption = (
        "📸 *Payment Proof Received*\n\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 User ID: `{user_id}`\n"
        f"📦 Plan: {plan[0]} ({plan[1]})"
    )

    keyboard = [
        [f"✅ Approve {user_id}", f"❌ Reject {user_id}"]
    ]

    update.message.forward(
        chat_id=ADMIN_ID
    )

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=caption,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    update.message.reply_text(
        "✅ Screenshot received.\nPlease wait for admin approval."
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
