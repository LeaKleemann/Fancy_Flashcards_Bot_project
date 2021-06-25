# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import json
import spacy
import pathlib

from sentence_transformers import SentenceTransformer, util
transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
def get_tensor(sentence):
    transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return transformer.encode(sentence,convert_to_tensor=True)
def encode_questions(df):
    df['q_tensor']=df.q.transform(get_tensor)
    return df
def encode_answers(df):
    df['a_tensor']=df.a.transform(get_tensor)
    return df


cwd_path=pathlib.Path().cwd()
data_path=cwd_path.joinpath('wirtschaftsinformatik-main/business-intelligence.json')
with open(data_path,encoding='utf-8') as f:
  data = json.load(f)

dftest=pd.DataFrame()

cwd_path=pathlib.Path().cwd()
data_path=cwd_path.joinpath('wirtschaftsinformatik-main')

deck_files=list(data_path.glob(r'*.json'))

deck_files

transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
frames=[]
for file in deck_files:
#     print(file)
    topic=file.stem
    with open(file,encoding='utf-8') as f:
        data = json.load(f)
    decks=data['decks']
    for deck in decks:
#         print(deck)
        cards=decks[deck]['cards']
        df=pd.DataFrame(cards)
        df=df.transpose()
        df=df.assign(topic=[topic for x in range(len(df.index))],deck=[deck for x in range(len(df.index))])
#         df['topic']=pd.Series([topic for x in range(len(df.index))], index=df.index)
#         df['deck']=pd.Series([deck for x in range(len(df.index))], index=df.index)
        df['q_tensor']=df.q.transform(get_tensor)
        df['a_tensor']=df.a.transform(get_tensor)
        frames.append(df)
        print('deck finished:',deck)
    print('topic finished:',topic)
dataframe=pd.concat(frames,axis=0)
# dataframe=encode_questions(dataframe)
# dataframe=encode_answers(dataframe)

dataframe.to_csv('data.csv',sep=';',index=False)

dataframe['q_tensor']=dataframe.q_tensor.transform(lambda x: x.tolist())
dataframe['a_tensor']=dataframe.q_tensor.transform(lambda x: x.tolist())

dataframe.head()

# +
from sqlalchemy import create_engine
db_file=cwd_path.joinpath('cards.db')

engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
dataframe = dataframe.applymap(str)
dataframe.to_sql('cards', con=engine,if_exists='replace')
# -

decks=data['decks']
# print('Number of decks: ',len(decks))
cards=decks['d1']['cards']
df=pd.DataFrame(cards)
df=df.transpose()

df.head()

# # spacy de_core_news_lg

df.a.iloc[0]

nlp=spacy.load('de_core_news_lg')
STOP_WORDS = spacy.lang.de.stop_words.STOP_WORDS

df.a.iloc[0]
a='Grund dafür sind Social Media,Activity Tracker und Transaktionen im Internet. Die zunehmende Digitalisierung führt zur zunehmenden Datenflut.'
doc3=nlp(a)

doc1=nlp(df.a.iloc[0])
doc2=nlp(df.a.iloc[1])

doc1.similarity(doc3)

index=0
answer=df.a.iloc[index]
similarities=[nlp(answer).similarity(nlp(df.a.iloc[x])) for x in range(len(df))]

similarities[8]

for i,similarity in enumerate(similarities):

    if similarity >= 0.75:
        print(i,'Gut gemacht! \n',answer)
    else:
        # print(i,'Schade!', answer)
        continue

# # tfidf via scikit-learn

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
import nltk
from HanTa import HanoverTagger as ht
import string
# nltk.download()

a=nltk.tokenize.word_tokenize(df.a.iloc[0],language='german')
b=ht.HanoverTagger('morphmodel_ger.pgz').tag_sent(a)

word,lemma,pos=b[6]

lemma


def preprocess(text):
    # tagger=HanTa.HanoverTagger('morphmodel_ger.pgz')
    a=ht.HanoverTagger('morphmodel_ger.pgz').tag_sent([text])
    # print(a)
    # print(len(a))
    return a[0]
def tokenizer(text):
    tokens=nltk.tokenize.word_tokenize(text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))),language='german')
    lemmas=[]
    # print(tokens)
    for token in tokens:
        word,lemma,pos=preprocess(token)
        lemmas.append(lemma)
    return lemmas



tagger=ht.HanoverTagger('morphmodel_ger.pgz')
tagger.tag_sent(['lief','Türen'])

xtrain,xtest,ytrain,ytest=train_test_split(df.q,df.a,test_size=0.33, random_state=1)

# + jupyter={"outputs_hidden": true}
stopwords=nltk.corpus.stopwords.words('german')
stemmer=nltk.stem.snowball.SnowballStemmer('german',ignore_stopwords=True)

tfidf=TfidfVectorizer(tokenizer=tokenizer)
transformer=tfidf.fit(xtrain)
xtraint=transformer.transform(xtest)
vocab=transformer.vocabulary_

# + jupyter={"outputs_hidden": true}
vocab=transformer.vocabulary_b
# -

# # sentence_transformer

# +
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

# Two lists of sentences
sentences1 = ['The cat sits outside',
             'A man is playing guitar',
             'The new movie is awesome']

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

#Compute cosine-similarits
cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

#Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
# -

transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

a='Die zunehmende Digitalisierung führt zur zunehmenden Datenflut. Social Media'
e1=transformer.encode(df.a.iloc[0],convert_to_tensor=True)
e2=transformer.encode(a,convert_to_tensor=True)

cosine_scores = util.pytorch_cos_sim(e1, e2)

cosine_scores.tolist()[0]

e_a=transformer.encode(df.a,convert_to_tensor=True)
cosine_scores = util.pytorch_cos_sim(e_a, e_a)


def get_tensor(sentence):
    return transformer.encode(sentence,convert_to_tensor=True)


df['tensor']=df.a.transform(get_tensor)

# + jupyter={"outputs_hidden": true}
for x,i in enumerate(df.tensor.head()):
    print(x,i)

# + jupyter={"outputs_hidden": true}
for t in df.tensor:
    print(type(t))
# -

cosine_scores = util.pytorch_cos_sim(df.tensor.iloc[0], df.tensor.iloc[1])


def get_similarities(tensor):
    cosine_scores=[]
    for t in df.tensor:
        cosine_score = util.pytorch_cos_sim(tensor, t)
        cosine_scores.append(cosine_score.tolist()[0])
    return cosine_scores


df['similarities']=df.tensor.transform(get_similarities)

np.argmax(df.similarities.iloc[4])

ind=df.index.tolist()
# ind=[str(x) for x in ind]

sims=pd.DataFrame(df.similarities.tolist(),columns=ind)

sims.head()
