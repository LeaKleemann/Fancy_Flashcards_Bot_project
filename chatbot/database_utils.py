
'''
This module contains functions regarding working with the sqlite database thats stores the flashcards.
'''

from sqlalchemy import create_engine
import pandas as pd
import pathlib2 as pathlib
import torch

cwd=pathlib.Path().cwd() # current working directory

db_file=cwd.joinpath('cards.db') # path for database


engine = create_engine('sqlite:///'+db_file.as_posix(), echo=False) # create the database engine for accessing data


def create_query(topic):
    '''
    Creates an SQL query that selects all cards from a specified topic.
    
    Input: topic (str) equal to the topic from the database
    
    Output: query (str) equal to an SQL query
    '''
    query='''SELECT * FROM cards WHERE topic="{}"'''.format(topic)
    return query
def transform_to_tensor(l):
    '''
    Helper function that translates the lists saved in the database back to a pytorch Floattensor.
    
    Input: l (string), string representation of a python list containing the pytorch tensors saved in the database
    
    Outout: torch.FloatTensor(l), transformed string into pytorch tensor 
    '''
    translation_table = dict.fromkeys(map(ord, '[] '), None)
    l=l.translate(translation_table) # remove brackets
    l=l.split(',')
    l=[float(x) for x in l] # create python list
    return torch.FloatTensor(l)
def read_data(topic):
    '''
    Reads cards of a specified topic from database and returns pandas dataframe.
    
    Input: topic (str) equal to the topic from the database
    
    Output: df (pandas DataFrame), containing q&a pairs and tensors
    '''
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
    '''
    returns a list of all topics from the database.
    
    Input: /
    
    Output: topics (list) of all topics in database
    '''
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
    '''
    Returns all question tensors.
    
    Input: /
    
    Output: torch.reshape(tensor[0], (1720,384)) (pytorch tensor), containing all question tensors
    '''
    query = '''SELECT * FROM questions;'''
    query_return = pd.read_sql_query(query, con=engine)
    df = pd.DataFrame(query_return)
    tensor=df.q_tensor.transform(transform_to_tensor)
    return torch.reshape(tensor[0], (1720,384))



def read_emd():
    '''
    Returns the entire database as DataFrame.
    
    Input: /
    
    Output: df (pandas DataFrame), containing all q&a pairs
    '''
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
