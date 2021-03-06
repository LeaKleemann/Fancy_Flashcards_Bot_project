#from typing import Text
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
import sentence_transf as S
from dotenv import load_dotenv

'''
load bot token and initialize bot
'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)

'''
fach= chosen topic
question= random question from bot
answer= answer from the user
sanswer= sample solution
nextq=Should learning be continued
atensor= Tensor of sample solution
'''
data = {'fach':"", 'question': "",  'answer': "", 'sanswer':"", 'nextq': "", 'atensor':""}
topicdf=pd.DataFrame()

'''define states for Handler'''
TOPIC=1
QUESTION = 2
ANSWER =3

'''get list of all topics'''
topics=dbu.get_topics()

'''
start lernen Command Handler
asks which topic the user wants to learn
Input: update, context
Return: chosen Topic state
'''
def lernen(update, context):
    
    global data
    keyboard=[]
    data = {'fach':"", 'question': "",  'answer': "", 'sanswer':"", 'nextq': "", 'atensor':""}
    
    
    for i in topics:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Wähle das Fach, das du lernen möchtest", reply_markup=markup)
    return TOPIC

'''
check which topic the user wants to learn
pick random question out of this topic and send question to user
Input: update, context 
Return: Question state
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
    print(data['sanswer'])
    data['atensor']=row.a_tensor
    update.message.reply_text(text=data['question'])
    return QUESTION

'''
get answer from user
check if user answerd to question or send question
check answer or answer the question from user
if cosinus similarty > 0.8 right answer else wrong answer
asks if user wants continue to learn or stop or choose new topic
Input: update, context
Return: Answer state
'''
def get_answer(update, context):
    data['answer']=update.message.text
    answer=data['answer'].lower()
    antwort=False
    
   
    for i in ["was ", "wo ", "wer ", "wie ", "wieso ", "wofür ", "wozu ", "wohin ", "warum ", "wem ", "woher "]:
        if i in answer:
            antwort=True
            S.get_answer(answer, update, bot)
            
    if not antwort:
        if data['answer']=="/help":
                path=True
                H.help(update, context, path)
                return ConversationHandler.END
        else:
            
            cossim=cau.compare_tensors(data['atensor'], answer)
            cossim=cossim[0]
            
            if cossim >=0.80:
                text_part= "Glückwünsch deine Antwort ist richtig "+  "\U0001F973"
                text_part2=text_part + "\U0001F913"
                text=text_part2+ "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
                
                update.message.reply_text(text=text)
                
            else:
                text_part= "Deine Antwort ist leider falsch oder unvollständig " + "\U0001F622"	
                text_part2=text_part + "\U0001F61F	"
                text=text_part2 + "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
                
                update.message.reply_text(text=text)
            
    


    keyboard=[]
    a=["Ja", "Nein", "Neues Thema lernen"]
    for i in a:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Möchtest du die nächste Frage bekommen?", reply_markup=markup)

    return ANSWER
    
'''
check if user wants to continue learning --> call get_type to choose next question
Input: update, context
Return:
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

'''
cancel Conversation Handler
Input: update, context
'''
def cancel(update, context):
    markup=ReplyKeyboardRemove()
    update.message.reply_text('Lernen beendet',reply_markup=markup)
    return ConversationHandler.END