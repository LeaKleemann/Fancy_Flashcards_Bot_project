# -*- coding: utf-8 -*-
#from Fancy_Flashcards_Bot_project.chatbot.learning import QUESTION
from telegram import *
from telegram.ext import *
import os
print(os.getcwd()) 
import responses as R
import timer as T
# import sentence_transf as S
import learning as L
import time

from dotenv import load_dotenv

import threading
from os import environ as env

# load token for telegram bot
load_dotenv()
#token=env["TELEGRAM_BOT_TOKEN"]
#token=os.environ.get("TELEGRAM_BOT_TOKEN")
token=os.getenv("TELEGRAM_BOT_TOKEN")
#print(token)
#token=keys.TELEGRAM_BOT_TOKEN
#token="1837522537:AAF0zbRUBKS3sl-0eQit2lweE5UKH7Vjh-0"
# initilize bot
bot=Bot(token)

print ("Bot strarted ...")



# data = {'title': "", 'text': "", 'comments': ""}
TYPE=1
TITLE = 2
TEXT = 3
COMMENTS = 4

def start_command(update,  context):
    bot.send_message(chat_id=update.message.chat_id, text="Herzlich Willkommenn! \n Der Fancy Flashcard Bot hilft dir beim Lernen. \n Wenn du hilfe brauchst gebe /help ein. \n Du willst das Fach aus wählen gebe /lernen ein. \n Zusätzlich kannst du dir einen Timer stellen. Das geht über /timer.")

def help_command(update,  context):
    bot.send_message(chat_id=update.message.chat_id, text="If you need help! You should ask for it on Google!")

def lernen_command(update,  context):

    markup=ReplyKeyboardMarkup([[KeyboardButton("Business Intelligence")],[KeyboardButton("Unternehmensführung")], 
     [KeyboardButton("Wirtschaftsinformatik")],[KeyboardButton("BWL") ]], resize_keyboard=True, one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id, reply_markup=markup,  text="Wähle das Fach welches du lernen möchtest \n - Business Intelligence \n - Unternehmensführung \n - Wirtschaftsinformatik \n - BWL")

# def timer_command (update, context):
    
#     #markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall")],[KeyboardButton("50:10 Intervall")]], resize_keyboard=True, one_time_keyboard=True)
#     #bot.send_message(chat_id=update.message.chat_id, text="Wähle das Pomodoro Intervall", reply_markup=markup)
#     x=threading.Thread(target=T.add,args=(update, context))
#     #update.message.reply_text(text="Timer Started")
#     x.start()



# def button(update: Update, context: CallbackContext) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
    
#     query.answer()
    
#     S.get_full_answer(query, update, bot)
#     return None
    


def handle_message(update, context):
    
    text = str(update.message.text).lower()
    print("Text:", text)
    print(f"Update Handle Message {update}")
    try:
        print("Reply:", update.message.reply_to_message)
    except:
        print("nicht vorhanden")

    #print(f"Update reply message {update.reply_to_message}")
    
    
    response=R.sample_responses(text, update, context)

    if response != None:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        

def error(update, context):
    print(f"Update {update} caused error {context.error}")






def main():  
    updater=Updater(token, use_context=True)
    dp=updater.dispatcher
    #print(dir(dp))
    # if gl_var==True:
    #     start_command()
    #     gl_var=False


    # lernen_conversation_handler=ConversationHandler(
    # entry_points=[CommandHandler('lernen', L.lernen)],
    # states={
    #     TYPE: [
    #         CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
    #         MessageHandler(Filters.text, L.get_type)
    #     ],
    #     QUESTION: [
    #         CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
    #         MessageHandler(Filters.text, L.get_answer)
    #     ],
    # },
    # fallbacks=[CommandHandler('cancel', L.cancel)]
    # )

    timer_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('timer', T.timer)],
    states={
        TYPE: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_type)
        ],
        TITLE: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_title)
        ],
        TEXT: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `text`
            MessageHandler(Filters.text, T.get_text)
        ],
        COMMENTS: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `comments`
            MessageHandler(Filters.text, T.get_comments)
        ],
    },
    fallbacks=[CommandHandler('cancel', T.cancel)]
    )                
#x=threading.Thread(target=R.timer,args=(update, context, data))
    dp.add_handler(timer_conversation_handler)
    #dp.add_handler(lernen_conversation_handler)
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("lernen", lernen_command)) 

    # dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    print('Running... [Press Ctrl+C to stop]')
    updater.idle()
    print('Stoping...')
    updater.stop()  
 
main()
