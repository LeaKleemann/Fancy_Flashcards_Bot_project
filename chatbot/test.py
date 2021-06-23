from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

TOKEN =

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# --- structure for data ---

data = {'title': "", 'text': "", 'comments': ""}

# --- states use in conversation ---

TITLE = 1
TEXT = 2
COMMENTS = 3

# --- functions use in conversation ---

# Command Handler which starts conversation
def add(update, context):
    global data # to assign new dictionary to external/global variable

    # create new empty dictionary
    data = {'title': "", 'text': "", 'comments': ""}

    update.message.reply_text("add title, text, comments in separated messages\n\nnow write title")

    # next state in conversation 
    return TITLE

def get_title(update, context):
    data['title'] = update.message.text

    update.message.reply_text(f"title: {update.message.text}\n\nnow write text")

    # next state in conversation 
    return TEXT

def get_text(update, context):
    data['text'] = update.message.text

    update.message.reply_text(f"text: {update.message.text}\n\nnow write comments")

    # next state in conversation 
    return COMMENTS

def get_comments(update, context):
    data['comments'] = update.message.text

    update.message.reply_text(f"comments: {update.message.text}")

    msg = """I got all data

title: {}
text: {}
comments: {}""".format(data['title'], data['text'], data['comments'])

    update.message.reply_text(msg)

    # end of conversation
    return ConversationHandler.END

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END

# --- create conversation ---

my_conversation_handler = ConversationHandler(
   entry_points=[CommandHandler('add', add)],
   states={
       TITLE: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
           MessageHandler(Filters.text, get_title)
       ],
       TEXT: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `text`
           MessageHandler(Filters.text, get_text)
       ],
       COMMENTS: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `comments`
           MessageHandler(Filters.text, get_comments)
       ],
   },
   fallbacks=[CommandHandler('cancel', cancel)]
)                

dispatcher.add_handler(my_conversation_handler)

# --- run bot ---

updater.start_polling()
print('Running... [Press Ctrl+C to stop]')
updater.idle()
print('Stoping...')
updater.stop()      