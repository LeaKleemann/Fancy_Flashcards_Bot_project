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


cwd=pathlib.Path().cwd()
db_file=cwd.joinpath('cards.db')
print(db_file)


# +
# engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)

# +
# engine
# -

def create_query(topic):
    query='''SELECT * FROM cards WHERE topic="{}"'''.format(topic)
    return query
def transform_to_tensor(l):
    translation_table = dict.fromkeys(map(ord, '[] '), None)
    l=l.translate(translation_table)
    l=l.split(',')
    l=[float(x) for x in l]
    return torch.FloatTensor(l)
def read_data(topic):
    engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    conn=engine.connect()
    q=create_query(topic)
    query=pd.read_sql_query(create_query(topic), con=engine)
    df = pd.DataFrame(query)
    df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
    df['a_tensor']=df.a_tensor.transform(transform_to_tensor)
    conn.close()
    engine.dispose()
    return df
def get_topics():
    engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    conn=engine.connect()
    querytopics='''SELECT DISTINCT topic FROM cards;'''
    queryt=pd.read_sql_query(querytopics, con=conn)
    dft = pd.DataFrame(queryt)
    topics=dft.topic.tolist()
    print(topics)
    conn.close()
    engine.dispose()
    return topics  


df=get_topics()

df

def read_emd():
    engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    conn=engine.connect()
    fquery='''SELECT * FROM cards'''
    #q=create_query("*")
    query=pd.read_sql_query(fquery, con=engine)
    df = pd.DataFrame(query)
    df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
    df['a_tensor']=df.a_tensor.transform(transform_to_tensor)
    conn.close()
    engine.dispose()
    return df
