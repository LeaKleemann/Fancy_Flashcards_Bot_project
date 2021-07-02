import pickle
from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import nltk
import spacy
from random import shuffle

'''load spacy model'''
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

'''define tokenizer for classifier,
input: sentence to tokenize,
output: dictionary with tokenized sentence'''
def spacy_tokenizer(question):
    doc = nlp(question)
    return_dict={}
    for token in doc:
        '''add lowercase nouns and poper nouns'''
        if token.pos_ in ["NOUN", "PROPN"]:
            text=token.text
            return_dict['contains({})'.format(text.lower())] = True
        '''add other words lemmatised and lowercase'''
        else:
            return_dict['contains({})'.format(token.lemma_.lower())] = True
    return return_dict

'''create dataframe'''
df = read_emd()

'''create and shuffle featureset'''
featuresets_question= [(spacy_tokenizer(question), 'question') for question in df['q']]
featuresets_answer= [(spacy_tokenizer(answer), 'no_question') for answer in df['a']]
featureset_train=featuresets_question+featuresets_answer
shuffle(featureset_train)
'''train classifier'''
classifier = nltk.NaiveBayesClassifier.train(featureset_train)
'''save classifier'''
f = open('naivebayes.pickle', 'wb')
pickle.dump(classifier, f)
f.close()