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
from github import Github
import ast
from sqlalchemy import create_engine

cwd=pathlib.Path().cwd()
# data_path=cwd.joinpath('wirtschaftsinformatik-main')
g = Github()
repo = g.get_repo("fancy-flashcard/deck-collection")
files = repo.get_contents("wirtschaftsinformatik")
db_file=cwd.joinpath('chatbot/cards.db')

# transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def get_tensor(sentence):
    # tensor=transformer.encode(sentence,convert_to_tensor=True)
    return transformer.encode(sentence,convert_to_tensor=True)
    # print(tensor)
    # return tensor
# def encode_questions(df):
#     df['q_tensor']=df.q.transform(get_tensor)
#     return df
# def encode_answers(df):
#     df['a_tensor']=df.a.transform(get_tensor)
#     return df
def read_json_files(files):
    frames=[]
    for file in files:
        topic=pathlib.Path(file.name).stem
        data=file.decoded_content.decode("UTF-8")
        data = ast.literal_eval(data)
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



# deck_files=list(data_path.glob(r'*.json'))
# test=[]
# test.append(deck_files[0])
# dataframe=read_json_files(test)
dataframe=read_json_files(files)

# +
engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)

dataframe['q_tensor']=dataframe.q_tensor.transform(lambda x: x.tolist())
dataframe['a_tensor']=dataframe.a_tensor.transform(lambda x: x.tolist())

dataframe = dataframe.applymap(str)

dataframe.to_sql('cards', con=engine,if_exists='replace')
dataframe.to_csv('data.csv',sep=';',index=False)
