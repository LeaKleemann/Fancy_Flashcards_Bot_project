# -*- coding: utf-8 -*-
from telegram import *
from telegram.ext import *
import os
print(os.getcwd()) 
import responses as R
import timer as T
import sentence_transf as S
import learning as L
import time
from dotenv import load_dotenv
import threading
from os import environ as env

'''load bot token and initialize Bot'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)

'''define states for Handlers
First Handler: Timer Handler
Second Handler: Learning Handler'''
TYPE=1
TITLE = 2
TEXT = 3
COMMENTS = 4

TOPIC=1
QUESTION=2
ANSWER=3

'''initialize start Command Handler, execution when user send message /start'''
def start_command(update,  context):
    
    text="Herzlich Willkommen beim Fancy Flashcard Bot!"+ u'⚡'+" Mit Hilfe von diesem Bot kannst du auf eine neue Art deine Karteikarten lernen."\
         + u'👩‍🎓' + u'👨‍🎓' + " Zum einen kannst du dem Bot Fragen stellen und er antwortet. Zum anderen ist es möglich, dass der Bot dir Fragen stellt.\
              Über das Keyboard kannst du diese Frage beantworten. Der Bot überprüft deine Antwort und korrigiert dich gegebenenfalls. \nDu \
                  benötigst Hilfe?" + u'❓'+" Gebe /help ein. \nDu willst Lernen." + u'🎓'+u'📚' \
                       +  "Geben /lernen ein und wähle das Fach aus, welches du lernen möchtest. \nZusätzlich kannst du dir einen Timer stellen."\
                            + u'⏱' +  "Den Timer startest du über /timer."

    bot.send_message(chat_id=update.message.chat_id, text=text)

'''initialize help Command Handler, execution when user send message /help'''
def help_command(update,  context):
    bot.send_message(chat_id=update.message.chat_id, text="If you need help! You should ask for it on Google!")


'''initialize Buttons for question to decide which question the user means
pass the question back to sentence transf to get the question and answer'''
def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    
    query.answer()
    
    S.get_full_answer(query, update, bot)
    return None
    
'''initialize Message handler 
every message is passed to sample responses to get the answer'''
def handle_message(update, context):
    
    text = str(update.message.text).lower()
    print("Text:", text)
    print(f"Update Handle Message {update}")
    response=R.sample_responses(text, update, context)

    if response != None:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        
'''error handler'''
def error(update, context):
    print(f"Update {update} caused error {context.error}")


'''start the chatbot
initialize Updater to get user messages'''
def main():  
    updater=Updater(token, use_context=True)
    dp=updater.dispatcher
    
    '''initilaze learning conversation Handler to control conversation'''
    lernen_conversation_handler=ConversationHandler(
    entry_points=[CommandHandler('lernen', L.lernen)],
    states={
        TOPIC: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, L.get_type)
        ],
        QUESTION: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, L.get_answer)
        ],
        ANSWER: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, L.next_question)
        ],
        # NEXT: [
        #     CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
        #     MessageHandler(Filters.text, L.next_question)
        # ],
    },
    fallbacks=[CommandHandler('cancel', L.cancel)]
    )

    '''initilaze timer conversation Handler to set a timer'''
    timer_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('timer', T.timer)],
    states={
        TYPE: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_type)
        ],
        TITLE: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_title)
        ],
        TEXT: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `text`
            MessageHandler(Filters.text, T.get_text)
        ],
        COMMENTS: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `comments`
            MessageHandler(Filters.text, T.get_comments)
        ],
    },
    fallbacks=[CommandHandler('cancel', T.cancel)]
    )                
#x=threading.Thread(target=R.timer,args=(update, context, data))
    
    '''add the different Handler'''
    dp.add_handler(timer_conversation_handler)
    dp.add_handler(lernen_conversation_handler)
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    #dp.add_handler(CommandHandler("lernen", lernen_command)) 

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    '''start bot'''
    updater.start_polling()
    print('Running... [Press Ctrl+C to stop]')
    updater.idle()
    print('Stoping...')
    updater.stop()  
 
main()
