import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6197033392

PAYMENT_TEXT = """
💳 **পেমেন্ট করুন**

**bKash Personal:** 01788371338
**Nagad Personal:** 01874511431

উপরের যেকোনো একটাতে Send Money করুন।
পেমেন্ট করে স্ক্রিনশট + আপনার নাম পাঠান।
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 পেমেন্ট করুন", callback_data="pay")],
        [InlineKeyboardButton("📞 এডমিন", url="https://t.me/BdTechpay")]
    ]
    await update.message.reply_text(f"স্বাগতম {update.effective_user.first_name}!\nVIP গ্রুপে জয়েন করতে পেমেন্ট করুন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "pay":
        await query.message.reply_text(PAYMENT_TEXT, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = f"🔔 নতুন পেমেন্ট প্রুফ\n👤 নাম: {user.first_name}\n🆔 ID: {user.id}\n🔗 @{user.username}"
    try:
        if update.message.photo:
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption)
        else:
            await context.bot.send_message(chat_id=ADMIN_ID, text=caption + f"\n\nমেসেজ: {update.message.text}")
        await update.message.reply_text("✅ আপনার প্রুফ এডমিনের কাছে গেছে। অনুগ্রহ করে অপেক্ষা করুন।")
    except Exception as e:
        print(e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
print("Bot Running...")
app.run_polling()
