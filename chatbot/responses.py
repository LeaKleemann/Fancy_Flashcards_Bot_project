from datetime import date, datetime
import time 
# import questiontfidf as Q
from telegram import *
from telegram.ext import * 
import os
import threading
from dotenv import load_dotenv
#import database_utils as dbu
import sentence_transf as S
from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import torch



# load token for telegram bot
#load_dotenv()
#token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
#bot=Bot(token)

#x=threading.Thread(target=funktion die aufgerufen werden soll)
#danachw weiter mit x.

def sample_responses(input_text, update, context):
    # cwd=pathlib.Path().cwd()
    # db_file=cwd.joinpath('cards.db')
    # print(db_file)

    # engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    # print(engine)

    load_dotenv()
    token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
    bot=Bot(token)


    user_message=input_text
    # #print(input_text)
    # for i in ["was", "wo", "wer", "wie", "wieso", "wofür", "wozu", "wohin", "warum", "wem", "woher","?"]:
    #     if i in user_message:
    #         print(user_message)
    #         #input_text=[input_text]
    #         S.get_answer(user_message, update, bot)
    #         return None
        
    
    if user_message in ("hello", "hi", "hallo"):
        print("func hallo")
        #topics=dbu.get_topics()
        #print(topics)        
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
                
        bot.send_message(chat_id=update.message.chat_id, text="Hey! How is it going?", reply_markup=ForceReply())
        
        return None

    if user_message in ("who are you", "who are you", "wer bist du" "wer bist du"):
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        bot.send_message(chat_id=update.message.chat_id, text="Ich bin ein Test Bot")
        return None
        

    if user_message in ("time", "time", "zeit", "zeit", "datum", "datum"):
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        now = datetime.now()
        date_time=now.strftime("%d/%m/%y, %H:%M:%S")
        date_time=str(date_time)
        bot.send_message(chat_id=update.message.chat_id, text=date_time)
        return None


    if user_message == "business intelligence":
       return "Du hast Business Intelligence gewählt"

    if user_message in "unternehmensführung":
        return"Du hast Unternehmensführung gewählt"

    if user_message == "wirtschaftsinformatik":
        return "Du hast Wirtschaftsinformatik gewählt"

    if user_message == "bwl":
        return"Du hast BWL gewählt"

    if user_message == "25:5 intervall":
        x=threading.Thread(target=timer,args=(bot,update))
        bot.send_message(chat_id=update.message.chat_id, text="Timer Started")
        x.start()
        
        return None

    return "I don't understand you."

def timer(update, context, data):
    worktime=int(data['worktime'])
    breaktime=int(data['breaktime'])
    wiederholugnen=int(data['wiederholungen'])
    for i in range(wiederholugnen):
        if i==0:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/work_time.png', 'rb'), caption="Start Working")
        t=worktime#*60
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            print(" " + timer, end="\r")
            time.sleep(1)
            t-=1
        if i==(wiederholugnen-1):
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/finish.png', 'rb'), caption="Finished Work")
        else:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/break_time.png', 'rb'), caption="Break Time")    
        t=breaktime#*60
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            print(" " + timer, end="\r")
            time.sleep(1)
            t-=1
        if i !=(wiederholugnen-1):
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/work_time.png', 'rb'), caption="Work Time")
        
    return None
    
