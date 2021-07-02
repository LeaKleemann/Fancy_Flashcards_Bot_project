from telegram import *
from telegram.ext import *
import learning as L
import os
from dotenv import load_dotenv
'''
load bot token and initialize bot
'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)
'''define help comand if user aks for help while he is in learning Command Handler'''
def help(update, context):
    text="Folgendes kannst du eingeben um mit dem Bot zu kommunizieren.\n"\
    "Wenn du Lernen möchtest gebe /lernen ein. Als erstes wirst du gefragt welches Deck " +u'📚'+ "du lernen möchtest."\
    "Über die automatisch erscheinenden Buttons kannst du das gewünschte Deck ganz einfach auswählen."\
    "Im Anschluss stellt dir der Bot eine zufällige Frage aus deinem gewähltem Deck. Diese Frage kannst du nun beantworten.\n\n"\
    "<b>WICHTIG:</b> Wenn du über Telegram Web lernst, wähle zunächst die Nachricht mit der Frage aus und drücke reply."\
    "Solltest du über die App lernen wird automatisch auf die Nachricht mir der Frage geantwortet."\
    "Das ist wichtig, damit der Bot überprüfen kann, ob deine Antwort richtig ist.\n\n"\
    "Im nächsten Schritt kriegst du vom Bot eine Rückmeldung ob deine Antwort richitg ist und wie die Musterlösung ist."\
    "Außerdem wirst du gefragt, ob du weiter lernen möchtest, aufhören möchtest oder das Deck wechseln möchtest. Hier kannst du wieder über die Buttons antworten."\
    "Solltest du Inhalte der Frage vom Bot nicht verstehen, lösche das Antworten auf die letzte Nachricht und tippe deine Frage ein."\
    "Der Bot antwortet dir nun auf deine Frage.\n\n"\
    "Wenn du eine Frage zu Inhalten der Decks hast, kannst du einfach deine Frage eintippen.\n\n"\
    "Außerdem kannst du dir einen Timer" + u'⏱' + "stellen während du lernst. Der Timer basiert auf der Promodoro Technick."\
    "Über /timer kannst du den Timer starten. Du kannst aus vordefinierten Timern wählen oder deinen eigenen Timer einstellen."\
    "Die Auswahlmöglichkeiten erscheinen über Buttons. Bei den vordefinierten  Timern wurde eine Arbeitszeit von 25 min bzw. 50 min festgelegt."\
    "Darauf folgt eine Pause von 5 min bzw. 10 min. Dieser Zyklus wird 2 mal wiederholt."\
    "Beim benutzerdefinierten Timer wirst du nach den jeweiligen Zeitintervallen und Wiederholungen gefragt. Antworte hier einfach mit deiner gewünschten Zahl."
    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
    L.cancel(update, context)