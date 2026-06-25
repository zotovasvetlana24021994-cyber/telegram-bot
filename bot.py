from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = "8725935673:AAFZ3_Fm3kAkr3RLTTSAXbzpcvLmbEQz5Dc"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# память
memory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет 👋 Я AI-бот (OpenAI). Пиши что угодно.")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory[update.effective_user.id] = []
    await update.message.reply_text("Память очищена 🧹")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        text = update.message.text

        if user_id not in memory:
            memory[user_id] = []

        memory[user_id].append({"role": "user", "content": text})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=memory[user_id][-10:]
        )

        answer = response.choices[0].message.content

        memory[user_id].append({"role": "assistant", "content": answer})

        await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("Ошибка AI")

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()