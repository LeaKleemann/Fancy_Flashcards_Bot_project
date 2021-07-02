import sqlalchemy
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pathlib2 as pathlib
import numpy as np
import json
from github import Github
import ast
from sqlalchemy import create_engine

'''create github object and get files'''
g = Github()
repo = g.get_repo("fancy-flashcard/deck-collection")
files = repo.get_contents("wirtschaftsinformatik")

'''get database file and create database engine'''
cwd=pathlib.Path().cwd()
db_file=cwd.joinpath('chatbot/cards.db')
engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)

'''define transformer model'''
transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

'''define function to get tensor of text'''
def get_tensor(sentence):
    return transformer.encode(sentence,convert_to_tensor=True)

'''define function to read content of files,
input: files from github,
output: dataframe with content of files and tensors of answers'''
def read_files(files):
    frames=[]
    for file in files:
        '''get decoded contet of file'''
        topic=pathlib.Path(file.name).stem
        data=file.decoded_content.decode("UTF-8")
        data = ast.literal_eval(data)
        decks=data['decks']
        '''create dataframe with questions and answers'''
        for deck in decks:
            cards=decks[deck]['cards']
            df=pd.DataFrame(cards)
            df=df.transpose()
            df=df.assign(topic=[topic for x in range(len(df.index))],deck=[deck for x in range(len(df.index))])
            '''create column with answer tensors'''
            df['a_tensor']=df.a.transform(get_tensor)
            frames.append(df)
            print('deck finished:',deck)
        print('topic finished:',topic)
    dataframe=pd.concat(frames,axis=0)
    return dataframe

'''get dataframe'''
dataframe=read_files(files)

'''convert tensors to string'''
dataframe['a_tensor']=dataframe.a_tensor.transform(lambda x: x.tolist())
dataframe = dataframe.applymap(str)

'''create question tensor and save in new dataframe'''
questions = get_tensor(dataframe['q'])
questions = str(questions.tolist())
questions_df = pd.DataFrame([questions], columns=["q_tensor"])

'''save tables to database'''
questions_df.to_sql('questions', con=engine, if_exists='replace')
dataframe.to_sql('cards', con=engine,if_exists='replace')

