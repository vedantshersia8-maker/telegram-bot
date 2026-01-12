import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram import ReplyKeyboardMarkup

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8498170357

# Store user selections in memory (simple)
user_plan = {}

def main_menu(update):
    keyboard = [
        ["ðŸ’° Purchase Subscription", "ðŸ“„ My Subscriptions"],
        ["ðŸ†˜ Contact Support", "ðŸ”„ Refresh Menu"]
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
        ["Basic - â‚¹500"],
        ["Premium Plus - â‚¹5000"],
        ["Private Reels - â‚¹2000"],
        ["VIP Users - â‚¹1000"],
        ["â¬… Back"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Available subscription plans:",
        reply_markup=reply_markup
    )

def show_payment_methods(update, plan_name, price):
    keyboard = [
        ["ðŸ‡®ðŸ‡³ Indian UPI Payment"],
        ["ðŸŒ International Payment"],
        ["âŒ Cancel"]
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
	
    if text.startswith("âœ… Approve"):
        user_id = int(text.split()[-1])
        context.bot.send_message(
            chat_id=user_id,
            text="ðŸŽ‰ Payment approved!\nYou will be added shortly."
        )
        update.message.reply_text("User approved âœ…")
        return

    if text.startswith("âŒ Reject"):
        user_id = int(text.split()[-1])
        context.bot.send_message(
            chat_id=user_id,
            text="âŒ Payment rejected.\nPlease contact support."
        )
        update.message.reply_text("User rejected âŒ")
        return


    if text == "ðŸ’° Purchase Subscription":
        show_plans(update)

    elif text == "ðŸ”„ Refresh Menu":
        main_menu(update)

    elif text == "â¬… Back":
        main_menu(update)

    elif text == "Basic - â‚¹500":
        user_plan[user_id] = ("Basic", "â‚¹500")
        update.message.reply_text(
            "ðŸ“¦ *Basic Plan*\n"
            "- Daily uploads of 2â€“3 pics/videos\n"
            "- Free demo available\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Basic", "â‚¹500")

    elif text == "Premium Plus - â‚¹5000":
        user_plan[user_id] = ("Premium Plus", "â‚¹5000")
        update.message.reply_text(
            "ðŸ“¦ *Premium Plus*\n"
            "- Access to premium group\n"
            "- Daily uploads\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Premium Plus", "â‚¹5000")

    elif text == "Private Reels - â‚¹2000":
        user_plan[user_id] = ("Private Reels", "â‚¹2000")
        update.message.reply_text(
            "ðŸ“¦ *Private Reels*\n"
            "- Unlimited reels\n"
            "- Daily uploads\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "Private Reels", "â‚¹2000")

    elif text == "VIP Users - â‚¹1000":
        user_plan[user_id] = ("VIP Users", "â‚¹1000")
        update.message.reply_text(
            "ðŸ“¦ *VIP Users*\n"
            "- Exclusive videos\n",
            parse_mode="Markdown"
        )
        show_payment_methods(update, "VIP Users", "â‚¹1000")

    elif text == "ðŸ‡®ðŸ‡³ Indian UPI Payment":
        plan = user_plan.get(user_id)
        if not plan:
            update.message.reply_text("Please select a plan first.")
            return

        update.message.reply_text(
            "ðŸ“² *UPI Payment*\n\n"
            "Send payment to:\n"
            "`paytm.s1axuq5@pty`\n\n"
            "After payment, send screenshot here.",
            parse_mode="Markdown"
        )

        # OPTIONAL: Send QR image
        # update.message.reply_photo(open("qr.png", "rb"))

    elif text == "ðŸŒ International Payment":
        update.message.reply_text(
            "ðŸŒ *International Payment*\n\n"
            "Payment via Remitly.\n"
            "Instructions will be shared soon.",
            parse_mode="Markdown"
        )

    elif text == "âŒ Cancel":
        main_menu(update)

    else:
        update.message.reply_text("Please use the menu buttons.")
		
def handle_photo(update, context):
    user = update.message.from_user
    user_id = user.id
    plan = user_plan.get(user_id, ("Unknown", "Unknown"))

    caption = (
        "ðŸ“¸ *Payment Proof Received*\n\n"
        f"ðŸ‘¤ User: {user.first_name}\n"
        f"ðŸ†” User ID: `{user_id}`\n"
        f"ðŸ“¦ Plan: {plan[0]} ({plan[1]})"
    )

    keyboard = [
        [f"âœ… Approve {user_id}", f"âŒ Reject {user_id}"]
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
        "âœ… Screenshot received.\nPlease wait for admin approval."
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()


if __name__ == "__main__":
    main()
