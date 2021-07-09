# -*- coding: utf-8 -*-
from telegram import *
from telegram.ext import *
import os 
import responses as R
import timer as T
import sentence_transf as S
import learning as L
import time
from dotenv import load_dotenv
import threading
import help as H

'''load bot token and initialize Bot'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)

'''
define states for Handlers
First Handler: Timer Handler
Second Handler: Learning Handler
'''
TYPE=1
WORK = 2
BREAK = 3
REPETITION = 4

TOPIC=1
QUESTION=2
ANSWER=3

'''initialize start Command Handler, execution when user send message /start
Input: update, context'''
def start_command(update,  context):
    
    text="Herzlich Willkommen beim Fancy Flashcard Bot! "+ u'⚡'+" Mit Hilfe von diesem Bot kannst du auf eine neue Art deine Karteikarten lernen."\
        + u'👩‍🎓' + u'👨‍🎓' + " Zum einen kannst du dem Bot Fragen stellen und er antwortet dir. Zum anderen ist es möglich, dass der Bot dir Fragen stellt. "\
        "Über das Keyboard kannst du diese Frage beantworten. Der Bot überprüft deine Antwort und korrigiert dich gegebenenfalls. \nDu benötigst Hilfe" + u'❓'+" Gib /help ein. \nDu willst Lernen?" + u'🎓'+u'📚' \
        + "Gib /lernen ein und wähle das Fach aus, welches du lernen möchtest. \nZusätzlich kannst du dir einen Timer stellen. "\
        + u'⏱' +  " Den Timer startest du über /timer."

    bot.send_message(chat_id=update.message.chat_id, text=text)

'''initialize help Command Handler, execution when user send message /help
Input: update, context'''
def help_command(update,  context):
    path=False
    H.help(update,context,path)

'''initialize cancel Command Handler, execution when user send message /cancel
Input: update, context'''
def cancel_command(update,  context):
    T.cancel(update,context)
    

'''initialize Buttons for question to decide which question the user means
pass the question back to sentence transf to get the question and answer
Input: update, context
Return: None'''
def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    S.get_full_answer(query, update, bot)
    return None
    
'''initialize Message handler 
every message is passed to sample responses to get the answer
Input: update, context'''
def handle_message(update, context):
    
    text = str(update.message.text).lower()
    response=R.sample_responses(text, update, context)

    if response != None:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        
'''error handler
Input: update, context'''
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
            CommandHandler('cancel', L.cancel),  
            MessageHandler(Filters.text, L.get_type)
        ],
        QUESTION: [
            CommandHandler('cancel', L.cancel),  
            MessageHandler(Filters.text, L.get_answer)
        ],
        ANSWER: [
            CommandHandler('cancel', L.cancel),  
            MessageHandler(Filters.text, L.next_question)
        ],
        
    },
    fallbacks=[CommandHandler('cancel', L.cancel)]
    )

    '''initilaze timer conversation Handler to set a timer'''
    timer_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('timer', T.timer)],
    states={
        TYPE: [
            CommandHandler('cancel', T.cancel),  
            MessageHandler(Filters.text, T.get_type)
        ],
        WORK: [
            CommandHandler('cancel', T.cancel),  
            MessageHandler(Filters.text, T.get_work)
        ],
        BREAK: [
            CommandHandler('cancel', T.cancel),  
            MessageHandler(Filters.text, T.get_break)
        ],
        REPETITION: [
            CommandHandler('cancel', T.cancel),  
            MessageHandler(Filters.text, T.get_repetition)
        ],
    },
    fallbacks=[CommandHandler('cancel', T.cancel)]
    )                

    
    '''add the different Handler'''
    dp.add_handler(timer_conversation_handler)
    dp.add_handler(lernen_conversation_handler)
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("cancel", cancel_command))
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
