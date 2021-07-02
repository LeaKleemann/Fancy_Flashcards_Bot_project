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
import help as H
#import main as M



# load token for telegram bot
#load_dotenv()
#token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
#bot=Bot(token)

#x=threading.Thread(target=funktion die aufgerufen werden soll)
#danachw weiter mit x.
def timer(update, context, data):
    worktime=int(data['worktime'])
    breaktime=int(data['breaktime'])
    wiederholugnen=int(data['wiederholungen'])
    for i in range(wiederholugnen):
        if i==0:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Fangen wir an zu lernen.")
        t=worktime#*60
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            print(" " + timer, end="\r")
            time.sleep(1)
            t-=1
        if i==(wiederholugnen-1):
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/finish.png', 'rb'), caption="Du hast es geschafft. Du bist fertig mit lernen.")
        else:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/break_time.png', 'rb'), caption="Zeit für eine Pause.")    
            t=breaktime#*60
            while t:
                mins = t // 60
                secs = t % 60
                timer = '{:02d}:{:02d}'.format(mins,secs)
                print(" " + timer, end="\r")
                time.sleep(1)
                t-=1
            #if i !=(wiederholugnen-1):
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Zeit zu lernen.")
            
    return None

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
    print(input_text)
    for i in ["was", "wo", "wer", "wie", "wieso", "wofür", "wozu", "wohin", "warum", "wem", "woher","?"]:
        if i in user_message:
            print(user_message)
            #input_text=[input_text]
            S.get_answer(user_message, update, bot)
            return None
        
    
    if user_message in ("hello", "hi", "hallo"):
        #print("func hallo")
        #topics=dbu.get_topics()
        #print(topics)        
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(1)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        text="Hey! Schön das du hier bist"+u'😃' + "\n Fangen wir an zu lernen!"
        bot.send_message(chat_id=update.message.chat_id, text=text)
        
        return None

    if user_message in ("wer bist du"):
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(1)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        text="Ich bin der Fancy Flashcard Bot" +u'⚡'+ "\n Ich helfe dir beim lernen." + u'🎓'+u'📚' + " \n Für weitere Infos Tippe /help ein."
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return None
        

    if user_message in ("zeit", "datum"):
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(1)        
        now = datetime.now()
        date_time=now.strftime("%d/%m/%y, %H:%M:%S")
        date_time=str(date_time)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
        bot.send_message(chat_id=update.message.chat_id, text=date_time)
        return None

    if user_message =="/help":
        H.help(update, context, bot )
        return None
    #     return ConversationHandler.END

    
    bot.send_message(chat_id=update.message.chat_id, text="Ich verstehe dich leider nicht. Für Hilfe gebe /help ein.")
    return None

# def timer(update, context, data):
#     worktime=int(data['worktime'])
#     breaktime=int(data['breaktime'])
#     wiederholugnen=int(data['wiederholungen'])
#     for i in range(wiederholugnen):
#         if i==0:
#             context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Fangen wir an zu lernen.")
#         t=worktime#*60
#         while t:
#             mins = t // 60
#             secs = t % 60
#             timer = '{:02d}:{:02d}'.format(mins,secs)
#             print(" " + timer, end="\r")
#             time.sleep(1)
#             t-=1
#         if i==(wiederholugnen-1):
#             context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/finish.png', 'rb'), caption="Du hast es geschafft. Du bist fertig mit lernen.")
#         else:
#             context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/break_time.png', 'rb'), caption="Zeit für eine Pause.")    
#             t=breaktime#*60
#             while t:
#                 mins = t // 60
#                 secs = t % 60
#                 timer = '{:02d}:{:02d}'.format(mins,secs)
#                 print(" " + timer, end="\r")
#                 time.sleep(1)
#                 t-=1
#             #if i !=(wiederholugnen-1):
#             context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Zeit zu lernen.")
            
#     return None
    
