import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# إعداد المفاتيح
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

openai.api_key = OPENROUTER_KEY
openai.api_base = "https://openrouter.ai/api/v1"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "أنت بنت دلع اسمك ساندي، بتتكلمي برقة ودلع، وبتعرفي تفرقي بين الجاد والهزار."},
            {"role": "user", "content": user_message}
        ]
    )
    reply_text = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply_text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot started...")
    app.run_polling()