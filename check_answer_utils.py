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
import random
from sentence_transformers import SentenceTransformer, util

transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def pick_random_question(df):
    length=len(df)-1
    index=random.randint(0,length)
    return index, df.iloc[index]
def get_tensor(sentence):
#     transformer=SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return transformer.encode(sentence,convert_to_tensor=True)
def compare_tensors(solution,answer):
    answer_tensor=get_tensor(answer)
    cosine_score = util.pytorch_cos_sim(solution, answer_tensor)
    return cosine_score.tolist()[0]
def get_answer_string(score):
    if score >=0.5:
        return 'Gut gemacht! Die Ähnlichkeit zur Musterlösung beträgt {}'.format(score)
    else:
        return 'Schade! Die Ähnlichkeit zur Musterlösung beträgt nur {}'.format(score)