from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sản phẩm của HeroTeam!", parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if update.message.chat.type != "private":
        if update.message.from_user.username in ["minatabar", "ChoOTCVN_support", "QuocPham_OTC"]:

            data = {'name': update.message.chat.title,
                    'group_id': update.message.chat.id}
            requests.post(f"{domain}/api/exchange-group", data)


        if update.message.chat.id == -863040168:
            if "/baogia" in update.message.text:
                text = update.message.text[8:]

                res = requests.get(f"{domain}/api/exchange-group")

                for item in res.json():
                    await context.bot.send_message(chat_id=item['group_id'], text=text, parse_mode=constants.ParseMode.HTML)


app = ApplicationBuilder().token(
    "5949578109:AAGzPN6EkNWfcYeO33ioKOB1EjB3hBW_sNQ").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()
