from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
import threading

token="1837522537:AAF0zbRUBKS3sl-0eQit2lweE5UKH7Vjh-0"
# initilize bot
#bot=Bot(token)

data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}
TYPE=1
TITLE = 2
TEXT = 3
COMMENTS = 4

def add(update, context):
    global data # to assign new dictionary to external/global variable

    # create new empty dictionary
    data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}


    markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall, 2 Wiederholungen")],[KeyboardButton("50:10 Intervall, 2 Wiederholungen")], [KeyboardButton("Benutzerdefiniert")]], resize_keyboard=True, one_time_keyboard=True)
    #bot.send_message(chat_id=update.message.chat_id, text="Wähle das Pomodoro Intervall", reply_markup=markup)
    update.message.reply_text(text="Wähle das Pomodoro Intervall", reply_markup=markup)

    # next state in conversation 
    return TYPE

def get_type(update,context):
    if update.message.text == "50:10 Intervall, 2 Wiederholungen":
        data2={'type':"50:10", 'worktime':50, 'breaktime':10, 'wiederholungen':2}
        msg = """I got all data
        type:{}
        worktime: {}
        breaktime: {}
        wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

        update.message.reply_text(msg)
        x=threading.Thread(target=R.timer,args=(update, context, data2))
        update.message.reply_text(text="Timer Started")
        x.start()
        return ConversationHandler.END
    
    elif update.message.text == "25:5 Intervall, 2 Wiederholungen":
        data2={'type':"25:5", 'worktime':25, 'breaktime':5, 'wiederholungen':2}
        msg = """I got all data
        type:{}
        worktime: {}
        breaktime: {}
        wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

        update.message.reply_text(msg)
        x=threading.Thread(target=R.timer,args=(update, context, data2))
        update.message.reply_text(text="Timer Started")
        x.start()
        return ConversationHandler.END
    
    
    else:
        data['type']=update.message.text
        update.message.reply_text(f"type: {update.message.text}\n\nnow write worktime")
        return TITLE

     


def get_title(update, context):
    data['worktime'] = update.message.text

    update.message.reply_text(f"worktime: {update.message.text}\n\nnow write breaktime")

    # next state in conversation 
    return TEXT

def get_text(update, context):
    data['breaktime'] = update.message.text

    update.message.reply_text(f"breaktime: {update.message.text}\n\nnow write wiederholungen")

    # next state in conversation 
    return COMMENTS

def get_comments(update, context):
    data['wiederholungen'] = update.message.text

    #update.message.reply_text(f"wiederholungen: {update.message.text}")

    msg = """I got all data
type:{}
worktime: {}
breaktime: {}
wiederholungen: {}""".format(data['type'],data['worktime'], data['breaktime'], data['wiederholungen'])

    update.message.reply_text(msg)
    x=threading.Thread(target=R.timer,args=(update, context, data))
    update.message.reply_text(text="Timer Started")
    x.start()
        
        

    # end of conversation
    return ConversationHandler.END

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END