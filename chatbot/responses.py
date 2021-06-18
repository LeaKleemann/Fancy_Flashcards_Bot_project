from datetime import date, datetime
import time 
import questiontfidf as Q
from telegram import *
from telegram.ext import * 
import os
import threading
from dotenv import load_dotenv

# load token for telegram bot
#load_dotenv()
#token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
#bot=Bot(token)

#x=threading.Thread(target=funktion die aufgerufen werden soll)
#danachw weiter mit x.

def sample_responses(input_text, update, context):

    load_dotenv()
    token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
    bot=Bot(token)


    user_message=input_text
    print(input_text)
    for i in ["was", "wo", "wer", "wie", "wieso", "wofür", "wozu", "wohin", "warum", "wem", "woher","?"]:
        if i in user_message:
            print("hallo")
            input_text=[input_text]
            Q.get_distance(input_text, update, bot)
            return None
        
    
    if user_message in ("hello", "hi", "hallo"):
                
        bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        time.sleep(2)
        bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
                
        bot.send_message(chat_id=update.message.chat_id, text="Hey! How is it going?")
        
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

def timer(bot, update):
    
    for i in range(1):
        t=25
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            print(" " + timer, end="\r")
            time.sleep(1)
            t-=1
        bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/break_time.png', 'rb'), caption="Break Time")    
        t=10
        while t:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins,secs)
            print(" " + timer, end="\r")
            time.sleep(1)
            t-=1
        bot.send_photo(chat_id=update.message.chat_id, photo=open('./Fancy_Flashcards_Bot_project/chatbot/work_time.png', 'rb'), caption="Work Time")
        
    return None
    
