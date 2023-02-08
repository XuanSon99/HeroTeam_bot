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
            if "/bg" in update.message.text:
                text = update.message.text[4:]

                res = requests.get(f"{domain}/api/exchange-group")

                list = []

                reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text='Xóa báo giá', callback_data='delete')]],)

                for item in res.json():
                    msg = await context.bot.send_message(chat_id=item['group_id'], text=text, parse_mode=constants.ParseMode.HTML)
                    list.append(msg.message_id)

                await context.bot.send_message(chat_id=-863040168, text=list, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = update.effective_message.id
    chat_id = update.effective_chat.id

    query = update.callback_query
    await query.answer()

    res = requests.get(f"{domain}/api/exchange-group")

    if query.data == "delete":
        msg = json.loads(update.effective_message.text)
        for index, item in enumerate(res.json()):
            await context.bot.delete_message(message_id=msg[index],
                                             chat_id=item['group_id'])

        await context.bot.delete_message(message_id=message_id, chat_id=chat_id)

app = ApplicationBuilder().token(
    "5949578109:AAGzPN6EkNWfcYeO33ioKOB1EjB3hBW_sNQ").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()
