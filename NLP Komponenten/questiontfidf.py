from spacy.lang.de import German
import spacy
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from telegram import *
from telegram.ext import * 
from dotenv import load_dotenv
import threading
import pathlib2 as pathlib
from sqlalchemy import create_engine
import pandas as pd
nlp = spacy.load('de_core_news_lg')

'''get database file'''
cwd=pathlib.Path().cwd()
db_file=cwd.joinpath('../chatbot/cards.db')

'''define function to get data from database,
output: dataframe that contains the data from the table cards'''
def read_emd():
    engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    conn=engine.connect()
    fquery='''SELECT * FROM cards'''
    query=pd.read_sql_query(fquery, con=engine)
    df = pd.DataFrame(query)
    engine.dispose()
    return df

modul=['business-intelligence', 'einfuehrung-in-die-wirtschaftsinformatik','Finanzbuchhaltung', 'finanzierung-und-investition', 'unternehmensfuehrung']
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")

#initilize bot
bot=Bot(token)

'''define tokenizer for tfidf,
input: message as string,
output: tokenized text as list'''
def spacy_tokenizer(message):
    doc = nlp(message)
    return_list=[]
    for token in doc:
        if token.pos_ != "PUNCT":
            if token.pos_ in ["NOUN", "PROPN"]:
                text=token.text
                return_list.append(text.lower())
            else:
                return_list.append(token.lemma_.lower())
    return return_list

def get_distance(message, update, bot):
    message=[message]
    '''get questions from database'''
    df=read_emd()

    '''define and train tfidf'''
    vectorizer = TfidfVectorizer(tokenizer=spacy_tokenizer)
    X = vectorizer.fit(df['q'])
    features = X.transform(df['q'])

    '''calculate tfidf vector for new message'''
    new_features = X.transform(message)
    '''calculate similarity to all questions'''
    cosine_sim = cosine_similarity(features, new_features)
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    '''get maximum value'''  
    max_idx=cosine_sim.argmax()
    best_question=all_questions[max_idx]
    cosinus_wert=cosine_sim[max_idx]
    


    for x in modul:
        modul_dict=fancy_flashcards[x]
        answer=modul_dict.get(best_question)
        if answer !=None:
            answer_f=answer
    
    text="Gefundene Frage \n" + best_question + "\n\n" +"Antwort \n" + answer_f
    bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
    bot.send_message(chat_id=update.message.chat_id, text=text)
    return None
