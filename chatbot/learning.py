from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
import threading
import database_utils as dbu

data = {'fach':"", 'question': "", 'answer': ""}
#fächer=["business-intelligence", "Einführung Wirtschaftsinformatik", "Finanzbuchhatung", "Finanzierung und Investition", "Unternehmensführung"]
TOPIC=1
QUESTION = 2
topics=dbu.get_topics()

def lernen(update, context):
    global data
    keyboard=[]
    data = {'fach':"", 'question': "", 'answer': ""}
    
    for i in topics:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Wähle das Fach das du lernen möchtst", reply_markup=markup)

    return TOPIC

def get_type(update, context):
    data['fach']=update.message.text
    print(data)
    for i in topics:
        if update.message.text == i:
             update.message.reply_text(text=i)

    question=dbu.get_question()
    data['question']=question
    update.message.reply_text(text=question, reply_markup=ForceReply())
    print(data)
    return QUESTION

# def check_question(update,context):
#     if update.message.reply_to_message !=None:


def get_answer(update, context):
    data['answer']=update.message.text
    answer=data['answer']
    if update.message.reply_to_message != None:
        
        print(data)
        result, korektanswer=dbu.check_answer(answer)
        if result == True:
            text="Glückwünsch deine Antwort ist richtig" + "\n" + "Das ist die Musterantwort:" + "\n" + korektanswer
            update.message.reply_text(text=text)
        else:
            text="Deine Antwort ist leider Falsch" + "\n" + "Das ist die Musterantwort:" + "\n" + korektanswer
            update.message.reply_text(text=text)
        '''zurücksetzen von question and answer'''
    else:
        R.sample_responses(data['answer'], update, context)
        '''zurücksetzen von question and answer'''
    #return get_type()
    return ConversationHandler.END

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END