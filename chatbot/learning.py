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
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
bot=Bot(token)
'''
fach= gewähltes Topic
question= random gewählte frage vom bot
qtensor=tensor der Frage
answer= antwort des users
atensor= tensor der musterlösung
sanswer= muster lösung
nextq=Soll lernen fortgesetzt werden
'''
data = {'fach':"", 'question': "",  'answer': "", 'sanswer':"", 'nextq': ""}
topicdf=pd.DataFrame()
#fächer=["business-intelligence", "Einführung Wirtschaftsinformatik", "Finanzbuchhatung", "Finanzierung und Investition", "Unternehmensführung"]
TOPIC=1
QUESTION = 2
ANSWER =3
#NEXT = 4
topics=dbu.get_topics()

def lernen(update, context):
    
    global data
    keyboard=[]
    data = {'fach':"", 'question': "", 'answer': "", 'sanswer':""}
    
    for i in topics:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
    update.message.reply_text(text="Wähle das Fach das du lernen möchtst", reply_markup=markup)

    return TOPIC

def get_type(update, context):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    global topicdf
    if update.message.text in topics:
    
        if data['fach'] == "": #or data['fach'] != topic:
            topic=update.message.text
            data['fach']=topic
            #print("fach leer")
    #data['fach']=update.message.text
    #print(data)
        for i in topics:
            if update.message.text == i:
                update.message.reply_text(text=i)
        topicdf=dbu.read_data(data['fach'])
    #df=topicdf
    index,row=cau.pick_random_question(topicdf)
    #print(index)
    #print(row)
    question=row.q
    data['question']=row.q
    #data['qtensor']=row.q_tensor
    #data['atensor']=row.a_tensor
    data['sanswer'] = row.a
    bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
    update.message.reply_text(text=question, reply_markup=ForceReply())
    print('Data:', data)
    return QUESTION

# def check_question(update,context):
#     if update.message.reply_to_message !=None:


def get_answer(update, context):
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    data['answer']=update.message.text
    answer=data['answer']
    if update.message.reply_to_message != None:
        
        print(data)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        cossim=cau.compare_tensors(data['sanswer'], answer)
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        cossim=cossim[0]
        print(cossim)
        #result, korektanswer=dbu.check_answer(answer)

        if cossim >=0.6:
            text_part= "Glückwünsch deine Antwort ist richtig "+  "\U0001F973"
            text_part2=text_part + "\U0001F913"
            text=text_part2+ "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
            bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
            update.message.reply_text(text=text)
            #check_next_question(update, context)
        else:
            text_part= "Deine Antwort ist leider Falsch " + "\U0001F622"	
            text_part2=text_part + "\U0001F61F	"
            text=text_part2 + "\n" + "Das ist die Musterantwort:" + "\n" + str(data['sanswer'])
            bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
            update.message.reply_text(text=text)
            #check_next_question(update,context)
    #bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")    
    else:
        R.sample_responses(data['answer'], update, context)


    keyboard=[]
    a=["Ja", "Nein", "Neues Thema lernen"]
    for i in a:
        keyboard.append([KeyboardButton(i)])
    markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Möchtest du die nächste Frage bekommen", reply_markup=markup)

    return ANSWER
    #return ConversationHandler.END
# def check_next_question(update,context):
#     keyboard=[]
#     a=["Ja", "Nein"]
#     for i in a:
#         keyboard.append([KeyboardButton(i)])
#     markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
#     bot.send_message(chat_id='788240189', text="Möchtest du die nächste Frage bekommen", reply_markup=markup)
#     return NEXT

def next_question(update, context):
    data['nextq']=update.message.text
    if data['nextq'] =='Ja':
        return get_type(update,context)
    if data['nextq']=="Neues Thema lernen":
        return lernen(update,context)
    else:
        update.message.reply_text('Lernen beendet')
        return ConversationHandler.END


def cancel(update, context):

    update.message.reply_text('Lernen beendet')

    # end of conversation
    return ConversationHandler.END