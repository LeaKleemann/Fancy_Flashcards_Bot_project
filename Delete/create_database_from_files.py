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

import sqlalchemy
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pathlib2 as pathlib
import numpy as np
import json
from sqlalchemy import create_engine

cwd=pathlib.Path().cwd()
data_path=cwd.joinpath('wirtschaftsinformatik-main')
db_file=cwd.joinpath('cards.db')

# transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def get_tensor(sentence):
    return transformer.encode(sentence,convert_to_tensor=True)
# def encode_questions(df):
#     df['q_tensor']=df.q.transform(get_tensor)
#     return df
# def encode_answers(df):
#     df['a_tensor']=df.a.transform(get_tensor)
#     return df
def read_json_files(deck_files):
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
    return dataframe



deck_files=list(data_path.glob(r'*.json'))
test=[]
test.append(deck_files[0])
dataframe=read_json_files(test)

# +
engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)

dataframe['q_tensor']=dataframe.q_tensor.transform(lambda x: x.tolist())
dataframe['a_tensor']=dataframe.q_tensor.transform(lambda x: x.tolist())

dataframe = dataframe.applymap(str)

dataframe.to_sql('cards', con=engine,if_exists='replace')
dataframe.to_csv('data.csv',sep=';',index=False)
