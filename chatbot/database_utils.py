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

from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import torch
import sqlite3

# cwd=pathlib.Path().cwd()
# print(cwd)
# db_file=cwd.joinpath('chatbot/cards.db')
# print(db_file)

# engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
# con=engine.connect()
# print(engine)


def create_query(topic):
    query='''SELECT * FROM cards WHERE topic="{}";'''.format(topic)
    return query
def transform_to_tensor(l):
    translation_table = dict.fromkeys(map(ord, '[] '), None)
    l=l.translate(translation_table)
    l=l.split(',')
    l=[float(x) for x in l]
    return torch.FloatTensor(l)
def read_data(engine,topic):
    q=create_query(topic)
    query=pd.read_sql_query(create_query(topic), con=engine)
    df = pd.DataFrame(query)
    df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
    df['a_tensor']=df.a_tensor.transform(transform_to_tensor)
    print(df)
    return df

def get_topics():
    topics=["business-intelligence", "Einführung Wirtschaftsinformatik", "Finanzbuchhatung", "Finanzierung und Investition", "Unternehmensführung"]
    # print(cwd)
    # print("func get topic")
    # querytopics='''SELECT DISTINCT topic FROM cards;'''
    # print(querytopics)
    # print(engine)
    # queryt=pd.read_sql_query(querytopics, con=con)
    # print("queryt")
    # dft = pd.DataFrame(queryt)
    # print("dft")
    # topics=dft.topic
    # print(topics)
    return topics

#print(get_topics())
def get_question():
    question="Welcher Tag ist heute?"
    return question

def check_answer(answer):
    korrektanswer="Heute ist Sonntag"
    if answer == korrektanswer:
        result =True
    else:
        result=False
    return result,korrektanswer
    