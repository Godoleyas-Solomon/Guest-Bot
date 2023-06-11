# -*- coding: utf-8 -*-

# Telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackContext, CallbackQueryHandler

# QR Code
from pyzbar.pyzbar import decode

# System libraries
from os import listdir
from os.path import isfile, join

from PIL import Image

import sqlite3
import config

TOKEN = config.token

conn = sqlite3.connect('guests.sqlite3')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS guests
             (id INTEGER PRIMARY KEY, code TEXT, first_name TEXT, last_name TEXT, family TEXT, checked INTEGER DEFAULT 0)''')


def decode_qr(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if update.message.photo:
        id_img = update.message.photo[-1].file_id
    else:
        return

    foto = context.bot.getFile(id_img)

    new_file = context.bot.get_file(foto.file_id)
    new_file.download('qrcode.png')

    try:
        result = decode(Image.open('qrcode.png'))
        code = result[0].data.decode("utf-8")

        # Create a new connection object
        with sqlite3.connect('guests.sqlite3') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM guests WHERE code=?", (code,))
            guest = c.fetchone()
            if guest:
                full_name = f"{guest[2]} {guest[3]}"
                family = guest[4] if guest[4] else "None"
                checked = guest[5]
                if checked:
                    message = f"Guest: {full_name}\nFamily: {family}\nChecked"
                    sent_message = context.bot.sendMessage(
                        chat_id=chat_id, text=message)
                else:
                    message = f"Guest: {full_name}\nFamily: {family}\nNot checked"
                    keyboard = [[InlineKeyboardButton("Check ✅", callback_data=f"check {code}")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    sent_message = context.bot.sendMessage(
                        chat_id=chat_id, text=message, reply_markup=reply_markup)
                    context.user_data[code] = sent_message.message_id
            else:
                sent_message = context.bot.sendMessage(
                    chat_id=chat_id, text='Guest doesn\'t exist', parse_mode='markdown')

    except Exception as e:
        context.bot.sendMessage(chat_id=chat_id, text=str(e))


def check_guest(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    code = query.data.split()[-1]
    message_id = context.user_data.get(code)
    if not message_id:
        return
    with sqlite3.connect('guests.sqlite3') as conn:
        c = conn.cursor()
        c.execute("UPDATE guests SET checked=1 WHERE code=?", (code,))
        conn.commit()
        guest = c.execute("SELECT * FROM guests WHERE code=?",
                          (code,)).fetchone()
        if guest:
            full_name = f"{guest[2]} {guest[3]}"
            family = guest[4] if guest[4] else "None"
            message = f"Guest: {full_name}\nFamily: {family}\nChecked"
            context.bot.editMessageText(chat_id=chat_id, message_id=message_id, text=message)
        else:
            context.bot.sendMessage(chat_id=chat_id, text="Code not found.")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is running")


def list_guests(update: Update, context: CallbackContext):
    with sqlite3.connect('guests.sqlite3') as conn:
        c = conn.cursor()
        guests = c.execute("SELECT * FROM guests ORDER BY first_name").fetchall()
        if guests:
            message = "```\n"
            message += "Code | First Name   | Last Name    | Family     | Checked\n"
            message += "-----|--------------|--------------|------------|--------\n"
            for guest in guests:
                code = guest[1]
                first_name = guest[2]
                last_name = guest[3]
                family = guest[4] if guest[4] else "None"
                checked = "✅" if guest[5] else "❌"
                message += f"{code} | {first_name:<12} | {last_name:<12} | {family:<10} | {checked}\n"
            message += "```"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='markdown')
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="No guests found.")


def list_checked_guests(update: Update, context: CallbackContext):
    with sqlite3.connect('guests.sqlite3') as conn:
        c = conn.cursor()
        guests = c.execute("SELECT * FROM guests WHERE checked=1 ORDER BY first_name").fetchall()
        if guests:
            message = "```\n"
            message += "Code | First Name   | Last Name    | Family     | Checked\n"
            message += "-----|--------------|--------------|------------|--------\n"
            for guest in guests:
                code = guest[1]
                first_name = guest[2]
                last_name = guest[3]
                family = guest[4] if guest[4] else "None"
                checked = "✅"
                message += f"{code} | {first_name:<12} | {last_name:<12} | {family:<10} | {checked}\n"
            message += "```"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='markdown')
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="No checked guests found.")


def main():
    updater = Updater(TOKEN, request_kwargs={
                      'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.photo, decode_qr))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('list', list_guests))
    dp.add_handler(CommandHandler('listchecked', list_checked_guests))
    dp.add_handler(CallbackQueryHandler(check_guest))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()