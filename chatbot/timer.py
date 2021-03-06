from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
import threading

'''define data dict to save user input'''
data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}

'''set states for Conversation Handler'''
TYPE=1
WORK = 2
BREAK = 3
REPETITION = 4

'''define timer 
ask for Timer Type
Input; update, context
Return: Type state'''
def timer(update, context):
    
    global data
    '''define data dict to save user inputs'''
    data = {'type':"",'worktime': "", 'breaktime': "", 'wiederholungen': ""}

    '''define Keyboard Markup so get Timer Type'''
    markup=ReplyKeyboardMarkup([[KeyboardButton("25:5 Intervall, 2 Wiederholungen")],[KeyboardButton("50:10 Intervall, 2 Wiederholungen")], [KeyboardButton("Benutzerdefiniert")]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Wähle das Pomodoro Intervall", reply_markup=markup)
 
    return TYPE

'''get timer type
if predefined timer start timer
else aks for worktime
Input: update, context
Return: work state'''
def get_type(update,context):
    markup=ReplyKeyboardRemove()
    #print(f"Update  get type {update}")
    if update.message.text == "50:10 Intervall, 2 Wiederholungen":
        data2={'type':"50:10", 'worktime':50, 'breaktime':10, 'wiederholungen':2}
        msg = """Ich habe alle Daten
        Typ:{}
        Arbeitszeit: {}
        Pausenzeit: {}
        Wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

        update.message.reply_text(msg, reply_markup=markup)
        x=threading.Thread(target=R.timer,args=(update, context, data2))
        update.message.reply_text(text="Timer gestartet")
        x.start()
        return ConversationHandler.END
    
    elif update.message.text == "25:5 Intervall, 2 Wiederholungen":
        data2={'type':"25:5", 'worktime':25, 'breaktime':5, 'wiederholungen':2}
        msg = """Ich habe alle Daten
        Typ:{}
        Arbeitszeit: {}
        Pausenzeit: {}
        Wiederholungen: {}""".format(data2['type'],data2['worktime'], data2['breaktime'], data2['wiederholungen'])

        update.message.reply_text(msg, reply_markup=markup)
        x=threading.Thread(target=R.timer,args=(update, context, data2))
        update.message.reply_text(text="Timer gestartet")
        x.start()
        return ConversationHandler.END
    
    
    else:
        data['type']=update.message.text
        update.message.reply_text(f"Typ: {update.message.text}\nGebe jetzt deine Arbeitszeit in Minuten ein", reply_markup=markup)
        return WORK

'''
get defined worktime from user message
ask for break time
Input: update, context
Return: break state
'''
def get_work(update, context):
    
    try:
        data['worktime'] = int(update.message.text)
    #if str.isdigit(data['worktime']):
        update.message.reply_text(f"Arbeitszeit: {update.message.text}\nGebe jetzt deine Pausenzeit in Minuten ein")
        return BREAK
    except:
        return cancel(update, context)

'''
get defined breaktime from user message
ask for repetitions
Input: update, context 
Return: repetition state
'''
def get_break(update, context):
    try:
        data['breaktime'] = int(update.message.text)
    #if str.isdigit(data['worktime']):
        update.message.reply_text(f"Pausenzeit: {update.message.text}\nGebe jetzt die Anzahl der Wiederholungen ein")
        return REPETITION
    except:
        return cancel(update, context)

'''
get defined repetition number from user message
start timer with defined numbers
Input: update, context
Return: End of Conversation Handler'''
def get_repetition(update, context):
    try:
        data['wiederholungen'] = update.message.text
    #if str.isdigit(data['worktime']):
        msg = """Ich habe alle Daten
    Typ:{}
    Arbeitszeit: {}
    Pausenzeit: {}
    Wiederholungen: {}""".format(data['type'],data['worktime'], data['breaktime'], data['wiederholungen'])

        update.message.reply_text(msg)
        x=threading.Thread(target=R.timer,args=(update, context, data))
        update.message.reply_text(text="Timer gestartet")
        x.start()
            

        return ConversationHandler.END
    except:
        return cancel(update, context)
'''
cancel timer Handler
Input: update, context
Return: End of Conversation Handler
'''
def cancel(update, context):

    update.message.reply_text('Timer beendet')

    # end of conversation
    return ConversationHandler.END