from typing import Text
from telegram import *
from telegram.ext import * 
import responses as R
import timer as T
import time
import os
import threading
import database_utils as dbu
import check_answer_utils as cau

import pandas as pd
import help as H



'''
fach= chosen topic
question= random question from bot
answer= answer from the user
sanswer= sample solution
nextq=Should learning be continued
'''
data = {'fach':"", 'question': "",  'answer': "", 'sanswer':"", 'nextq': ""}
topicdf=pd.DataFrame()

'''define states for Handler'''
TOPIC=1
QUESTION = 2
ANSWER =3

'''get list of all topics'''
topics=dbu.get_topics()

'''
start lernen Command Handler
aks which topic the user wants to learn
return chosen Topic state
'''
def lernen(update, context):
    
    global data
    keyboard=[]
    data = {'fach':"", 'question': "", 'answer': "", 'sanswer':""}
    
    for i in topics:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Wähle das Fach das du lernen möchtst", reply_markup=markup)
    return TOPIC

'''
check which topic the user wants to learn
pick random question out of this topic
send question to user and force reply
return Question state
'''
def get_type(update, context):
    markup=ReplyKeyboardRemove()
    global topicdf
    if update.message.text in topics:
    
        if data['fach'] == "": 
            topic=update.message.text
            data['fach']=topic
            
        for i in topics:
            if update.message.text == i:
                update.message.reply_text(text=i, reply_markup=markup)
        topicdf=dbu.read_data(data['fach'])
   
    index,row=cau.pick_random_question(topicdf)
    question=row.q
    data['question']=row.q
    data['sanswer'] = row.a
    update.message.reply_text(text=question, reply_markup=ForceReply())
    return QUESTION

'''
get answer from user
check if user answerd to question or send question
check answer or answer the question from user
if cosinus similarty > 0.6 right answer else wrong answer
aks if user wants continue to learn or stop or choose new topic
return Answer state
'''
def get_answer(update, context):
    data['answer']=update.message.text
    answer=data['answer']
    if update.message.reply_to_message != None:
        cossim=cau.compare_tensors(data['sanswer'], answer)
        cossim=cossim[0]
        
        if cossim >=0.6:
            text_part= "Glückwünsch deine Antwort ist richtig "+  "\U0001F973"
            text_part2=text_part + "\U0001F913"
            text=text_part2+ "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
            
            update.message.reply_text(text=text)
            
        else:
            text_part= "Deine Antwort ist leider Falsch " + "\U0001F622"	
            text_part2=text_part + "\U0001F61F	"
            text=text_part2 + "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
            
            update.message.reply_text(text=text)
            
    else:
        if data['answer']=="/help":
            H.help(update, context)
            return ConversationHandler.END
        else:
            R.sample_responses(data['answer'], update, context)


    keyboard=[]
    a=["Ja", "Nein", "Neues Thema lernen"]
    for i in a:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Möchtest du die nächste Frage bekommen", reply_markup=markup)

    return ANSWER
    
'''
check if user wants to continue learning --> call get_type to choose next question
if user wants to choose new topic --> call lernen
or if user wants to end learning --> end Conversation handler
'''
def next_question(update, context):
    markup=ReplyKeyboardRemove()
    data['nextq']=update.message.text
    if data['nextq'] =='Ja':
        return get_type(update,context)
    if data['nextq']=="Neues Thema lernen":
        return lernen(update,context)
    else:
        update.message.reply_text('Lernen beendet', reply_markup=markup)
        return ConversationHandler.END

'''cancel Conversation Handler'''
def cancel(update, context):
    markup=ReplyKeyboardRemove()
    update.message.reply_text('Lernen beendet',reply_markup=markup)

    # end of conversation
    return ConversationHandler.END