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
from os import environ as env
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

#     text="Folgendes kannst du eingeben um mit dem Bot zu kommunizieren.\n"\
# "Wenn du Lernen möchtest gebe /lernen ein. Als erstes wirst du gefragt welches Deck " +u'📚'+ "du lernen möchtest."\
# "Über die automatisch erscheinenden Buttons kannst du das gewünschte Deck ganz einfach auswählen."\
# "Im Anschluss stellt dir der Bot eine zufällige Frage aus deinem gewähltem Deck. Diese Frage kannst du nun beantworten.\n\n"\
# "<b>WICHTIG:</b> Wenn du über Telegram Web lernst, wähle zunächst die Nachricht mit der Frage aus und drücke reply."\
# "Solltest du über die App lernen wird automatisch auf die Nachricht mit der Frage geantwortet."\
# "Das ist wichtig, damit der Bot überprüfen kann, ob deine Antwort richtig ist.\n\n"\
# "Im nächsten Schritt kriegst du vom Bot eine Rückmeldung ob deine Antwort richitg ist und wie die Musterlösung ist."\
# "Außerdem wirst du gefragt, ob du weiter lernen möchtest, aufhören möchtest oder das Deck wechseln möchtest. Hier kannst du wieder über die Buttons antworten."\
# "Solltest du Inhalte der Frage vom Bot nicht verstehen, lösche das Antworten auf die letzte Nachricht und tippe deine Frage ein."\
# "Der Bot antwortet dir nun auf deine Frage.\n\n"\
# "Wenn du eine Frage zu Inhalten der Decks hast, kannst du einfach deine Frage eintippen."\
# "Sollte sich der Bot nicht sicher sein welche Frage gemeint ist, erscheinen Auswahlbuttons."\
# "Nach Auswahl der gewünschten Frage antwortet der Bot auf die gewählte Frage.\n\n"\
# "Außerdem kannst du dir einen Timer" + u'⏱' + "stellen während du lernst. Der Timer basiert auf der Promodoro Technick."\
# "Über /timer kannst du den Timer starten. Du kannst aus vordefinierten Timern wählen oder deinen eigenen Timer einstellen."\
# "Die Auswahlmöglichkeiten erscheinen über Buttons. Bei den vordefinierten  Timern wurde eine Arbeitszeit von 25 min bzw. 50 min festgelegt."\
# "Darauf folgt eine Pause von 5 min bzw. 10 min. Dieser Zyklus wird 2 mal wiederholt."\
# "Beim benutzerdefinierten Timer wirst du nach den jeweiligen Zeitintervallen und Wiederholungen gefragt. Antworte hier einfach mit deiner gewünschten Zahl."
#     bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
    path=False
    H.help(update,context,path)
    


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
            CommandHandler('cancel', L.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, L.get_type)
        ],
        QUESTION: [
            CommandHandler('cancel', L.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, L.get_answer)
        ],
        ANSWER: [
            CommandHandler('cancel', L.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
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
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_type)
        ],
        WORK: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
            MessageHandler(Filters.text, T.get_work)
        ],
        BREAK: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `text`
            MessageHandler(Filters.text, T.get_break)
        ],
        REPETITION: [
            CommandHandler('cancel', T.cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `comments`
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
