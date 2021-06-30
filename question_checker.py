import pickle
import spacy
nlp = spacy.load('de_core_news_lg')

def spacy_tokenizer(question):
    doc = nlp(question)
    return_dict={}
    for token in doc:
        # if token.pos_ != "PUNCT":
        if token.pos_ in ["NOUN", "PROPN"]:
            text=token.text
            return_dict['contains({})'.format(text.lower())] = True
        else:
            return_dict['contains({})'.format(token.lemma_.lower())] = True
    return return_dict

f = open('naivebayes.pickle', 'rb')

classifier = pickle.load(f)

f.close()

sentence="Wer bist du"
print(classifier.classify(spacy_tokenizer(sentence)))