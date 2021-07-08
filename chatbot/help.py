from telegram import *
from telegram.ext import *
import learning as L
import os
from dotenv import load_dotenv

'''load bot token and initialize bot'''
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")
bot=Bot(token)

'''define help comand if user aks for help 
check from which Handler the help function is called
if the user ask for help out of the Learning Handler Learning Conversation Handler is canceld
Input: update, context, path'''
def help(update, context, path):
    text="Folgendes kannst du eingeben um mit dem Bot zu kommunizieren.\n"\
    "Wenn du Lernen möchtest gebe /lernen ein. Als erstes wirst du gefragt welches Deck " +u'📚'+ "du lernen möchtest. "\
    "Über die automatisch erscheinenden Buttons kannst du das gewünschte Deck ganz einfach auswählen. "\
    "Im Anschluss stellt dir der Bot eine zufällige Frage aus deinem gewähltem Deck. Diese Frage kannst du nun beantworten.\n"\
    "Im nächsten Schritt kriegst du vom Bot eine Rückmeldung, ob deine Antwort richtig ist und wie die Musterlösung ist. "\
    "Außerdem wirst du gefragt, ob du weiter lernen möchtest, aufhören möchtest oder das Deck wechseln möchtest. Hier kannst du wieder über die Buttons antworten. "\
    "Solltest du Inhalte der Frage vom Bot nicht verstehen, tippe einfach deine Frage ein. "\
    "Der Bot antwortet dir nun auf deine Frage.\n"\
    "Sollte sich der Bot nicht sicher sein welche Frage du meinst erscheinen Auswahlbuttons. "\
    "Nach Auswahl der gewünschten Frage antwortet der Bot auf die gewählte Frage.\n"\
    "Außerdem kannst du dir einen Timer" + u'⏱' + " stellen während du lernst. Der Timer basiert auf der Promodoro Technik. "\
    "Über /timer kannst du den Timer starten. Du kannst aus vordefinierten Timern wählen oder deinen eigenen Timer einstellen. "\
    "Die Auswahlmöglichkeiten erscheinen über Buttons. Bei den vordefinierten  Timern wurde eine Arbeitszeit von 25 min bzw. 50 min festgelegt. "\
    "Darauf folgt eine Pause von 5 min bzw. 10 min. Dieser Zyklus wird 2 mal wiederholt. "\
    "Beim benutzerdefinierten Timer wirst du nach den jeweiligen Zeitintervallen und Wiederholungen gefragt. Antworte hier einfach mit deiner gewünschten Zahl an Minuten."
    bot.send_message(chat_id=update.message.chat_id, text=text)
    if path:
        L.cancel(update, context)