import numpy as np
# import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter

def createcloud(res):
    collection = ''
    for i in res:
        collection += str(i['text'])

    total_tokens = word_tokenize(collection)
    total_tokens2 = []
    for word in total_tokens:
        word = word.lower()
        if word not in stopwords.words('english'):
            total_tokens2.append(word)

    counted_1 = Counter(total_tokens2).most_common()
    counted_2 = Counter(ngrams(total_tokens2, 2)).most_common()
    counted_3 = Counter(ngrams(total_tokens2, 3)).most_common()

    return dict(counted_1), dict(counted_2), dict(counted_3)