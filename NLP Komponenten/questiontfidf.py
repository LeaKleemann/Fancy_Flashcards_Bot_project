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

def get_distance(message):
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
    '''get maximum value'''  
    max_idx=cosine_sim.argmax()
    best_question=df['q'][max_idx]
    cosinus_wert=cosine_sim[max_idx]
    return best_question, cosinus_wert
    


'''define and get similar question'''
sentence="Was ist BI?"
print(get_distance(sentence))