import numpy as np
import pandas as pd
from telegram import *
from telegram.ext import *
from sentence_transformers import SentenceTransformer, util
from telegram import ForceReply, replymarkup
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from sklearn.metrics.pairwise import cosine_similarity
import torch
import database_utils as dbu
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

'''get all questions with answers and question tensor from database'''
embeddings=dbu.read_emd()
corpus_embeddings = dbu.get_question_tensor()

'''define function get_answer, 
input: questions from user, 
output: answer to question if similarity is high, three nearest questions to choose when similarity is low'''

answers=[]
def get_answer(frage, update, bot):
    '''calculate question embedding and calculate similarity to all questions from database'''
    query_embedding = model.encode(frage)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=1)
    #print(top_results[0])
    '''if similarity is high: get answer to question and send this answer to user'''
    if float(top_results[0]) >= 0.80:
        answer= embeddings["q"][int(top_results[1])]
        an=embeddings['a'][int(top_results[1])]
        answer=answer+ "\n" + an 
        bot.send_message(chat_id=update.message.chat_id, text=answer)

        '''low similarity: send three nearest questions and let user choose which answer should be sent'''
    else:
        top_results = torch.topk(cos_scores, k=3)
        global answers
        botanswer=""
        keyboard=[]
        '''create list with answers'''
        for i in range(len(top_results[0])):
            answer=embeddings["q"][int(top_results[1][i])], str(float(top_results[0][i])), str(int(top_results[1][i]))
            answers.append(answer)
            
        '''create keyboard with found questions'''
        for j in range(len(answers)):
            for i in range(2):
                botanswer += answers[j][i]
                botanswer += " "
                if i ==0:
                    keyboard.append([InlineKeyboardButton(answers[j][i], callback_data=j)])
                if i == 1:
                    botanswer += "\n"
                
        reply_markup = InlineKeyboardMarkup(keyboard)
        '''send keyboard to user'''
        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    return None

'''
define function
input: query data
output: send question and answer to user
'''
def get_full_answer(query, update, bot):
    index=int(answers[int(query.data)][2])
    q=str(answers[int(query.data)][0])
    an=embeddings['a'][index]
    query.edit_message_text(text=f"Selected option: {q} \n Answer: {an}")
    answers.clear()
    return None 