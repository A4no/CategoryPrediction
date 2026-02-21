from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import predicttion as prd


TOKEN = "8487158411:AAFailIAkyei1neBkmvHICsK7_9nVB6QR94"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your news And this bot say that type")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    prediction_text = update.message.text
    pred = prd.Predict(prediction_text)
    await update.message.reply_text(f'your message type is: {pred[0]}')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Bot-ը աշխատում է...")
app.run_polling()
