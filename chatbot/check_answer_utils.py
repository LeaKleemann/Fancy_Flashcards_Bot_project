'''
This module contains functions regarding the mode in which the user wants to be asked a question and have is answer checked.
'''

import pandas as pd
import numpy as np
import torch
import random
from sentence_transformers import SentenceTransformer, util

transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # the sentence-transformer model used
def pick_random_question(df):
    '''
    Chooses a random question from the data
    
    Input: df (pandas DataFrame), containing cards q&a pairs of the current topic selected
    
    Output: tuple, index (int) DataFrame index of question choosen,  row of DataFrame at index
    '''
    length=len(df)-1
    index=random.randint(0,length)
    return index, df.iloc[index]

def get_tensor(sentence):
    '''
    Transform answer-string to pytorch tensor
    
    Input: sentence (str), answer given by user
    
    Output: transformer.encode(sentence,convert_to_tensor=True) (pytorch tensor), tensor representation of answer
    '''
#     transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return transformer.encode(sentence,convert_to_tensor=True)

def compare_tensors(solution,answer):
    '''
    Compare the solution to the answer given and return cosine-score
    
    Input: solution (str) sample solution, answer (str) answer given by user
    '''
    answer_tensor=get_tensor(answer)
    #solution_tensor=get_tensor(solution)
    cosine_score = util.pytorch_cos_sim(solution, answer_tensor)[0] # get cosine-score
    top_results = torch.topk(cosine_score, k=1) # choose top result
    return top_results

