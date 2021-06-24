import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

embeddings= np.loadtxt("embeddings.txt")
embeddings = embeddings.astype(np.float32)
corpus_embeddings = torch.from_numpy(embeddings)

df = pd.read_csv("questions_answers.csv")

def get_answer(frage):
    query_embedding = model.encode(frage, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=1)
    # return df["question"][int(top_results[1])] # gibt ähnlichste frage zurück
    return df["question"][int(top_results[1])] # gibt antwort zurück

frage="Was ist Data Mining?"
print(get_answer(frage))