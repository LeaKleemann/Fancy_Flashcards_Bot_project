# -*- coding: utf-8 -*-
from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
from dotenv import load_dotenv
#from dotenv import load_dotenv
import threading
from os import environ as env
# load token for telegram bot
load_dotenv()
#token=env["TELEGRAM_BOT_TOKEN"]
#token=os.environ.get("TELEGRAM_BOT_TOKEN")
#token=os.getenv("TELEGRAM_BOT_TOKEN")
#print(token)
#token=keys.TELEGRAM_BOT_TOKEN
token="1837522537:AAF0zbRUBKS3sl-0eQit2lweE5UKH7Vjh-0"
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

def timer_command (update, context):
    
    #markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall")],[KeyboardButton("50:10 Intervall")]], resize_keyboard=True, one_time_keyboard=True)
    #bot.send_message(chat_id=update.message.chat_id, text="Wähle das Pomodoro Intervall", reply_markup=markup)
    x=threading.Thread(target=T.add,args=(update, context))
    #update.message.reply_text(text="Timer Started")
    x.start()

def handle_message(update, context):
    
    text = str(update.message.text).lower()
    print(text)
    #print(f"Update {update}")
    #text=[text]
    
    # if text == "25:5 intervall":
    #     for i in range(1):
    #         bot.send_message(chat_id=update.message.chat_id, text="Timer gestartet")
    #         time.sleep(25)
    #         bot.send_message(chat_id=update.message.chat_id, text="Break Time!!")
    #         time.sleep(10)
    #         bot.send_message(chat_id=update.message.chat_id, text="Work Time")
    #else:        
        
    response=R.sample_responses(text, update, context)

    if response != None:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        

def error(update, context):
    print(f"Update {update} caused error {context.error}")


# data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}

# def add(update, context):
#     global data # to assign new dictionary to external/global variable

#     # create new empty dictionary
#     data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}


#     markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall, 2 Wiederholungen")],[KeyboardButton("50:10 Intervall, 2 Wiederholungen")], [KeyboardButton("Benutzerdefiniert")]], resize_keyboard=True, one_time_keyboard=True)
#     #bot.send_message(chat_id=update.message.chat_id, text="Wähle das Pomodoro Intervall", reply_markup=markup)
#     update.message.reply_text(text="Wähle das Pomodoro Intervall", reply_markup=markup)

#     # next state in conversation 
#     return TYPE

# def get_type(update,context):
#     if update.message.text == "50:10 Intervall, 2 Wiederholungen":
#         data2={'type':"50:10", 'worktime':50, 'breaktime':10, 'wiederholungen':2}
#         msg = """I got all data
#         type:{}
#         worktime: {}
#         breaktime: {}
#         wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

#         update.message.reply_text(msg)
#         x=threading.Thread(target=R.timer,args=(update, context, data2))
#         update.message.reply_text(text="Timer Started")
#         x.start()
#         return ConversationHandler.END
    
#     elif update.message.text == "25:5 Intervall, 2 Wiederholungen":
#         data2={'type':"25:5", 'worktime':25, 'breaktime':5, 'wiederholungen':2}
#         msg = """I got all data
#         type:{}
#         worktime: {}
#         breaktime: {}
#         wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

#         update.message.reply_text(msg)
#         x=threading.Thread(target=R.timer,args=(update, context, data2))
#         update.message.reply_text(text="Timer Started")
#         x.start()
#         return ConversationHandler.END
        
    
    
#     else:
#         data['type']=update.message.text
#         update.message.reply_text(f"type: {update.message.text}\n\nnow write worktime")
#         return TITLE

     


# def get_title(update, context):
#     data['worktime'] = update.message.text

#     update.message.reply_text(f"worktime: {update.message.text}\n\nnow write breaktime")

#     # next state in conversation 
#     return TEXT

# def get_text(update, context):
#     data['breaktime'] = update.message.text

#     update.message.reply_text(f"breaktime: {update.message.text}\n\nnow write wiederholungen")

#     # next state in conversation 
#     return COMMENTS

# def get_comments(update, context):
#     data['wiederholungen'] = update.message.text

#     #update.message.reply_text(f"wiederholungen: {update.message.text}")

#     msg = """I got all data
# type:{}
# worktime: {}
# breaktime: {}
# wiederholungen: {}""".format(data['type'],data['worktime'], data['breaktime'], data['wiederholungen'])

#     update.message.reply_text(msg)
#     x=threading.Thread(target=R.timer,args=(update, context, data))
#     update.message.reply_text(text="Timer Started")
#     x.start()
        
        

#     # end of conversation
#     return ConversationHandler.END

# def cancel(update, context):

#     update.message.reply_text('canceled')

#     # end of conversation
#     return ConversationHandler.END


def main():  
    updater=Updater(token, use_context=True)
    dp=updater.dispatcher
    #print(dir(dp))
    # if gl_var==True:
    #     start_command()
    #     gl_var=False




    my_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('add', T.add)],
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
    dp.add_handler(my_conversation_handler)
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("lernen", lernen_command))
    dp.add_handler(CommandHandler("timer", timer_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    print('Running... [Press Ctrl+C to stop]')
    updater.idle()
    print('Stoping...')
    updater.stop()  
 
main()
