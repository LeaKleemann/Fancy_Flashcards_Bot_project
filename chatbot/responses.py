from datetime import date, datetime
import time 
from telegram import *
from telegram.ext import * 
import os
import threading
from dotenv import load_dotenv
import sentence_transf as S
from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import torch
import help as H

'''load bot token and initialize Bot'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)

'''define timer, calculate worktime and breaktime'''
def timer(update, context, data):
    
    worktime=int(data['worktime'])
    breaktime=int(data['breaktime'])
    wiederholugnen=int(data['wiederholungen'])
    for i in range(wiederholugnen):
        if i==0:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Fangen wir an zu lernen.")
        t=worktime*60
        '''calculate worktime'''
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            time.sleep(1)
            t-=1
        if i==(wiederholugnen-1):
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/finish.png', 'rb'), caption="Du hast es geschafft. Du bist fertig mit lernen.")
        else:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/break_time.png', 'rb'), caption="Zeit für eine Pause.")    
            t=breaktime*60
            '''calculate break time'''
            while t:
                mins = t // 60
                secs = t % 60
                timer = '{:02d}:{:02d}'.format(mins,secs)
                time.sleep(1)
                t-=1
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/work_time.png', 'rb'), caption="Zeit zu lernen.")       
    return None

'''function to handle responses, check what the user messages was
Input: user text, update, context
Return: Depends on checking'''
def sample_responses(input_text, update, context):
    

    user_message=input_text

    '''defined answer if user message is hello, hi or hallo
    send answer to user
    return None'''
    if user_message in ("hello", "hi", "hallo"):       
        text="Hey! Schön dass du hier bist "+u'😃' + "\nFangen wir an zu lernen!"
        bot.send_message(chat_id=update.message.chat_id, text=text)
        
        return None

    '''defined answer if user message is wer bist du
    send answer to user
    return None'''
    if user_message in ("wer bist du", "wer bist du?"):
        text="Ich bin der Fancy Flashcard Bot" +u'⚡'+ "\nIch helfe dir beim lernen." + u'🎓'+u'📚' + " \nFür weitere Infos tippe /help ein."
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return None

    '''defined answer if user message is zeit or datum and send answer to user
    Return: None'''
    if user_message in ("zeit", "datum"):       
        now = datetime.now()
        date_time=now.strftime("%d/%m/%y, %H:%M:%S")
        date_time=str(date_time)
        bot.send_message(chat_id=update.message.chat_id, text=date_time)
        return None

    '''if the user message is a question answer this with the help of sentence transf
    Return: None'''
    for i in ["was ", "wo ", "wer ", "wie ", "wieso ", "wofür ", "wozu ", "wohin ", "warum ", "wem ", "woher "]:
        if i in user_message:
            
            S.get_answer(user_message, update, bot)
            
            return None
        
    
    '''if user message =/help answer the message with the help of help function
    Return: None'''
    if user_message =="/help":
        H.help(update, context)
        return None

    '''if no match found answer with the following text
    Return: None '''       
    bot.send_message(chat_id=update.message.chat_id, text="Ich verstehe dich leider nicht. Für Hilfe gebe /help ein.")
    return None


    
