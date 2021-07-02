import pickle
import spacy
nlp = spacy.load('de_core_news_lg')

'''define tokenizer for classifier,
input: sentence to tokenize,
output: dictionary with tokenized sentence'''
def spacy_tokenizer(sentence):
    doc = nlp(sentence)
    return_dict={}
    for token in doc:
        '''add lowercase nouns and poper nouns'''
        if token.pos_ in ["NOUN", "PROPN"]:
            text=token.text
            return_dict['contains({})'.format(text.lower())] = True
        '''add other words lemmatised and lowercase'''
        else:
            return_dict['contains({})'.format(token.lemma_.lower())] = True
    return return_dict

'''load saved classifier'''
f = open('naivebayes.pickle', 'rb')
classifier = pickle.load(f)
f.close()

'''define and classify a sentence'''
sentence="Data Management ist ein Teil von Business Intelligence"
print(classifier.classify(spacy_tokenizer(sentence)))