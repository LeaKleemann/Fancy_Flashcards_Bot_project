from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
import threading

data = {'fach':"", 'question': "", 'answer': ""}
fächer=["business-intelligence", "Einführung Wirtschaftsinformatik", "Finanzbuchhatung", "Finanzierung und Investition", "Unternehmensführung"]
TYPE=1
QUESTION = 2


def lernen(update, context):
    global data
    keyboard=[]
    data = {'fach':""}
    for i in fächer:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Wähle das Fach das du lernen möchtst", reply_markup=markup)

    return TYPE

def get_type(update, context):
    data['type']=update.message.text
    for i in fächer:
        if update.message.text == i:
             update.message.reply_text(text=i)
    question='''get random question'''
    data['question']=question
    update.message.reply_text(text=question, reply_markup=ForceReply())
    return QUESTION        

def get_answer(update, context):
    if update.message.reply_to_message != None:
        data['answer']=update.message.text
        result, korektanswer='''überprüfen der Antwort'''
        if result == True:
            update.message.reply_text()
        else:
            update.message.reply(text=falsch+korektanswer)
        '''zurücksetzen von question and answer'''
    else:
        R.sample_responses(data['answer'], update, context)
        '''zurücksetzen von question and answer'''
    return get_type()

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END