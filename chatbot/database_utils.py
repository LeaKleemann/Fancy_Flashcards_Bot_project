from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import torch

cwd=pathlib.Path().cwd()

db_file=cwd.joinpath('cards.db')


engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)


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
    print(df['a_tensor'][0])
    # df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
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


def get_question_tensor():
    query = '''SELECT * FROM questions;'''
    query_return = pd.read_sql_query(query, con=engine)
    df = pd.DataFrame(query_return)
    tensor=df.q_tensor.transform(transform_to_tensor)
    return torch.reshape(tensor[0], (1720,384))



def read_emd():
    engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False)
    conn=engine.connect()
    fquery='''SELECT * FROM cards'''
    #q=create_query("*")
    query=pd.read_sql_query(fquery, con=engine)
    df = pd.DataFrame(query)
    # df['q_tensor']=df.q_tensor.transform(transform_to_tensor)
    df['a_tensor']=df.a_tensor.transform(transform_to_tensor)
    conn.close()
    engine.dispose()
    return df
