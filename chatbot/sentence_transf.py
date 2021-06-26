import numpy as np
import pandas as pd
from telegram import *
from telegram.ext import *
from sentence_transformers import SentenceTransformer, util
from telegram import ForceReply, replymarkup
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
import torch
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

embeddings= np.loadtxt('Fancy_Flashcards_Bot_project\chatbot\embeddings.txt')
embeddings = embeddings.astype(np.float32)
corpus_embeddings = torch.from_numpy(embeddings)

df = pd.read_csv("Fancy_Flashcards_Bot_project\chatbot\questions_answers.csv")
answers=[]
def get_answer(frage, update, bot):
    query_embedding = model.encode(frage, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=1)
    print(top_results[0])
    if float(top_results[0]) >= 0.60:
        answer= df["question"][int(top_results[1])]
        an=df['answer'][int(top_results[1])] # gibt antwort zurück
        answer=answer+ "\n" + an 
        bot.send_message(chat_id=update.message.chat_id, text=answer)
    else:
        top_results = torch.topk(cos_scores, k=3)
        global answers
        botanswer=""
        keyboard=[]
        for i in range(len(top_results[0])):
            answer=df["question"][int(top_results[1][i])], str(float(top_results[0][i])), str(int(top_results[1][i]))
            answers.append(answer)
            print(answers)
        for j in range(len(answers)):
            for i in range(2):
                botanswer += answers[j][i]
                botanswer += " "
                if i ==0:
                    keyboard.append([InlineKeyboardButton(answers[j][i], callback_data=j)])
                if i == 1:
                    botanswer += "\n"
                
        
       

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)


    
    
    return None

def get_full_answer(query, update, bot):
    print((int(query.data)))
    print(answers)
    index=int(answers[int(query.data)][2])
    q=answers[int(query.data)][0]
    print(type(index))
    an=df['answer'][index]
    print(an)
    query.edit_message_text(text=f"Selected option: {q} \n Answer: {an}")
    answers.clear()
    return None 