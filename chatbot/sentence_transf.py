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
#model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

embeddings=dbu.read_emd()
corpus_embeddings = dbu.get_question_tensor()
#corpus_embeddings = corpus_embeddings.astype(np.float32)
#embeddings= np.loadtxt(r'embeddings.txt')

#corpus_embeddings = torch.from_numpy(embeddings)

#df = pd.read_csv(r"questions_answers.csv")

answers=[]
def get_answer(frage, update, bot):
    query_embedding = model.encode(frage)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=1)
    print(top_results[0])
    if float(top_results[0]) >= 0.60:
        answer= embeddings["q"][int(top_results[1])]
        an=embeddings['a'][int(top_results[1])]
        answer=answer+ "\n" + an 
        bot.send_message(chat_id=update.message.chat_id, text=answer)
    else:
        top_results = torch.topk(cos_scores, k=3)
        global answers
        botanswer=""
        keyboard=[]
        for i in range(len(top_results[0])):
            answer=embeddings["q"][int(top_results[1][i])], str(float(top_results[0][i])), str(int(top_results[1][i]))
            answers.append(answer)
            print("Answers:",answers)
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
    print("Query Data:",int(query.data))
    print("Answer full:", answers)
    index=int(answers[int(query.data)][2])
    print(index)
    q=str(answers[int(query.data)][0])
    print("q:",q)
    #print(type(index))
    print("embeddings:", embeddings['a'][index])
    an=embeddings['a'][index]
    print(type(an))
    print("an:",an)
    query.edit_message_text(text=f"Selected option: {q} \n Answer: {an}")
    answers.clear()
    return None 