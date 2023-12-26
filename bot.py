from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import time
from ast import literal_eval

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://api.chootc.com"
token = "6950786800:AAHCI-8R29qkTC5_fIG44fGfKp6uu2FV2rY"
manage_group_id = -4004349904


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Sản phẩm của HeroTeam!", parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    res = requests.get(
        f"https://api.telegram.org/bot{token}/getMe")
    username_bot = res.json()['result']['username']

    data = {'name': update.message.chat.title,
            'group_id': update.message.chat.id,
            'key': username_bot + str(update.message.chat.id),
            'username': username_bot}

    requests.post(f"{domain}/api/group", data)

    if update.message.chat.type == "private":
        return

    if "/" == update.message.text[:1]:    
        if update.message.chat.id == manage_group_id:
        
            res = requests.get(f"{domain}/api/groups/{username_bot}")

            list = []

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Xóa', callback_data='delete')]],)

            for index, item in enumerate(res.json()):
                if item['type'] == update.message.text[:2]:
                    try:
                        text = update.message.text[3:].lower()
                        if "chị" in item['name'].lower():
                            text = text.replace("anh","chị")
                        msg = await context.bot.send_message(chat_id=item['group_id'], text=text, parse_mode=constants.ParseMode.HTML)
                        list.append(msg.message_id)
                    except:
                        requests.delete(f"{domain}/api/group/{item['id']}")
                        pass

                if (index + 1) % 8 == 0:
                    time.sleep(2)

            await context.bot.send_message(chat_id=manage_group_id, text=list, reply_markup=reply_markup)
    
    else:
        try:
            text = update.message.text

            if "+" in text:
                arr = text.split("+")
                cal = "+"
            if "-" in text:
                arr = text.split("-")
                cal = "-"
            if "*" in text:
                arr = text.split("*")
                cal = "*"
            if "/" in text:
                arr = text.split("/")
                cal = "/"

            first_num = literal_eval(arr[0].replace(",","").strip())
            last_num = literal_eval(arr[1].replace(",","").strip())
            result = eval(text.replace(",",""))

            msg = f'{first_num:,} {cal} {last_num:,} = {result:,}'

            await context.bot.send_message(chat_id, text=msg, parse_mode=constants.ParseMode.HTML)
        except:
            result = eval(text.replace(",",""))

            msg = f'{text} = {result:,}'

            await context.bot.send_message(chat_id, text=msg, parse_mode=constants.ParseMode.HTML)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = update.effective_message.id
    chat_id = update.effective_chat.id

    query = update.callback_query
    await query.answer()

    res = requests.get(
        f"https://api.telegram.org/bot{token}/getMe")
    username_bot = res.json()['result']['username']

    res = requests.get(f"{domain}/api/groups/{username_bot}")

    if query.data == "delete":
        msg = json.loads(update.effective_message.text)
        for index, item in enumerate(res.json()):
            try:
                await context.bot.delete_message(message_id=msg[index], chat_id=item['group_id'])
            except:
                pass
            
            if (index + 1) % 8 == 0:
                time.sleep(2)

        await context.bot.delete_message(message_id=message_id, chat_id=chat_id)

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()
