# -*- coding: utf-8 -*-
from telegram import *
from telegram.ext import * 
import responses as R
import sys
import time
import os
from dotenv import load_dotenv

# load token for telegram bot
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
bot=Bot(token)

print ("Bot strarted ...")

def start_command(update,  context):
    bot.send_message(chat_id=update.message.chat_id, text="Herzlich Willkommenn! \n Der Fancy Flashcard Bot hilft dir beim Lernen. \n Wenn du hilfe brauchst gebe /help ein. \n Du willst das Fach aus wählen gebe /lernen ein. \n Zusätzlich kannst du dir einen Timer stellen. Das geht über /timer.")

def help_command(update,  context):
    bot.send_message(chat_id=update.message.chat_id, text="If you need help! You should ask for it on Google!")

def lernen_command(update,  context):

    markup=ReplyKeyboardMarkup([[KeyboardButton("Business Intelligence")],[KeyboardButton("Unternehmensführung")], 
     [KeyboardButton("Wirtschaftsinformatik")],[KeyboardButton("BWL") ]], resize_keyboard=True, one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id, reply_markup=markup,  text="Wähle das Fach welches du lernen möchtest \n - Business Intelligence \n - Unternehmensführung \n - Wirtschaftsinformatik \n - BWL")

def timer_command (update, context):
    
    markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall")],[KeyboardButton("50:10 Intervall")]], resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Wähle das Pomodoro Intervall", reply_markup=markup)

def handle_message(update,  context):
    #print(f"Text {update} parameter {context.CallbackContext}")
    #text=[update.message.text]
    text = str(update.message.text).lower()
    text=[text]
    print(text)
    if text == "25:5 intervall":
        for i in range(1):
            bot.send_message(chat_id=update.message.chat_id, text="Timer gestartet")
            time.sleep(25)
            bot.send_message(chat_id=update.message.chat_id, text="Break Time!!")
            time.sleep(10)
            bot.send_message(chat_id=update.message.chat_id, text="Work Time")
    else:        
        response=R.sample_responses(text)
        bot.send_message(chat_id=update.message.chat_id, text=response)
        #bot.send_message(chat_id=update.message.chat_id)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():    
    updater=Updater(token, use_context=True)
    dp=updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("lernen", lernen_command))
    dp.add_handler(CommandHandler("timer", timer_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    # if update:
    #     if message.text == "unternehmensführung":
    #         last_command = message.text

    updater.start_polling()
    updater.idle()

main()