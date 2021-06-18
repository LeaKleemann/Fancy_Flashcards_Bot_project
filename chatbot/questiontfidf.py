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

nlp = spacy.load('de_core_news_sm')

os.chdir('C:\\Studium\\Studium_Dokumente\\6. Semester\\DS Entwicklungen Projekt')

all_questions=[]
fancy_flashcards = {}
path='./wirtschaftsinformatik'
for file in os.listdir(path):
    file_path=path+'/'+file
    file_list=file.split('.')
    #print(file_list)
    if file_list[-1]=='json':
        with open(file_path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            temp_dict = {}
            decks=list(data['decks'].keys())
            cards=data['decks'][decks[0]]['cards']
            for index in cards.keys():
                temp_dict[cards[index]['q']]=cards[index]['a']
                all_questions.append(cards[index]['q'])
            fancy_flashcards[file_list[0]]=temp_dict
modul=['business-intelligence', 'einfuehrung-in-die-wirtschaftsinformatik','Finanzbuchhaltung', 'finanzierung-und-investition', 'unternehmensfuehrung']
load_dotenv()
token=os.getenv("TELEGRAM_BOT_TOKEN")


# initilize bot
bot=Bot(token)


#def question_distance(input_text_resp, all_questions):
#message=input_text_resp
    
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

    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")  
    print("get distance", message)

    vectorizer = TfidfVectorizer(tokenizer=spacy_tokenizer)
    X = vectorizer.fit(all_questions)
    features = X.transform(all_questions)


    new_features = X.transform(message)
    cosine_sim = cosine_similarity(features, new_features)
    bot.send_chat_action(chat_id=update.message.chat_id, action="typing")  
    max_idx=cosine_sim.argmax()
    best_question=all_questions[max_idx]
    cosinus_wert=cosine_sim[max_idx]
    print("best_question", best_question)
    print("wert", cosinus_wert)
    
    bot.send_message(chat_id=update.message.chat_id, text=best_question)
    text=' '.join([str(item) for item in message])
    
    for x in modul:
        modul_dict=fancy_flashcards[x]
        answer=modul_dict.get(best_question)
        if answer !=None:
            answer_f=answer
    bot.send_chat_action(chat_id=update.message.chat_id, action="cancel")
    bot.send_message(chat_id=update.message.chat_id, text=answer_f)
    return None
    #return best_question, cosinus_wert

      
    
#best_question, cosinus_wert = get_distance(all_questions, message, bot)
    # print("best_question", best_question)
    # print("wert", cosinus_wert)
    # return best_question, cosinus_wert





#text="Was führt zu einer zunehmenden Datenflut/ Big Data??"
