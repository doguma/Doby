import spacy
import re
import markovify
import nltk
import warnings
warnings.filterwarnings('ignore')

def random_sentence(collection):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(collection)
    sents = ' '.join([sent.text for sent in doc.sents if len(sent.text) > 1])

    gen1 = markovify.Text(sents, state_size=3)

    sent_list = []
    for i in range(3):
        sent_list.append(gen1.make_short_sentence(max_chars=100))

    return sent_list