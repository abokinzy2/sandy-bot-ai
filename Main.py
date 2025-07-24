import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توكن التليجرام
BOT_TOKEN = "8405035725:AAGt-bmkIYw54Og9RB5NzTuS2Og7cbGHQH4"

# إعداد اللوج
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الجمل المفتاحية
CASH_REQUIRED = "للتعامل لازم يكون عندك محفظة كاش. عندك؟ (نعم/لا)"
ASK_PROOF = "ابعت سكرين شوت لمحفظتك 💼"
GIVE_GIRL = "تمام. ده حساب ساندي: @SandYy48"
REJECT = "آسفة، بنتعامل مع الجادين بس 💔"

# ذاكرة بسيطة للمستخدمين
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا، معك ساندي 💅\n" + CASH_REQUIRED)
    user_states[update.effective_user.id] = "ask_cash"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    state = user_states.get(user_id)

    if state == "ask_cash":
        if "نعم" in text or "عندي" in text:
            await update.message.reply_text(ASK_PROOF)
            user_states[user_id] = "wait_proof"
        else:
            await update.message.reply_text(REJECT)
            user_states[user_id] = "rejected"

    elif state == "wait_proof":
        if update.message.photo:
            await update.message.reply_text(GIVE_GIRL)
            user_states[user_id] = "done"
        else:
            await update.message.reply_text("لازم تبعت صورة تثبت إن عندك محفظة.")

    else:
        await update.message.reply_text("اكتب /start نبدأ من الأول.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

app.run_polling()
