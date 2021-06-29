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

cwd=pathlib.Path().cwd()
# print(cwd)
db_file=cwd.joinpath('cards.db')
# print(db_file)

engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
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
def read_data(topic):
    q=create_query(topic)
    query=pd.read_sql_query(create_query(topic), con=engine)
    df = pd.DataFrame(query)
    print(df['a_tensor'][0])
    # df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
    df['a_tensor']=df.a_tensor.transform(transform_to_tensor)
    return df

def get_topics():
#     print("func get topic")
    querytopics='''SELECT DISTINCT topic FROM cards;'''
#     print(querytopics)
    queryt=pd.read_sql_query(querytopics, con=engine)
#     print("queryt")
    dft = pd.DataFrame(queryt)
#     print("dft")
    topics=dft.topic
#     print(topics)
    return topics

def get_question_tensor():
    query = '''SELECT * FROM questions;'''
    query_return = pd.read_sql_query(query, con=engine)
    df = pd.DataFrame(query_return)
    tensor=df.q_tensor.transform(transform_to_tensor)
    return tensor[0]

print(get_question_tensor())
# print(read_data("Finanzbuchhaltung"))
