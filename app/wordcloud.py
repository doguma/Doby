import re
import numpy as np
# import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter


blank_words = ['disease', 'background', 'reports', 'may', 'changes', 'report', 'suggested', 'exte', 'development', 'association', '\'s']


			


def createcloud_trendy(res):
    collection = ''
    for i in res:
        collection += str(i['text_full'])

    total_tokens = word_tokenize(collection)
    total_tokens2 = []
    total_tokens3 = []
    for word in total_tokens:
        word = re.sub("[^\w\d'\s_-]+", '', word).strip()
        word = word.lower()
        if word not in stopwords.words('english') and len(word)>1 and word not in blank_words:
            total_tokens2.append(word)

    for word in total_tokens:
        word = re.sub("[^\w\d'\s_-]+", '', word).strip()
        word = word.lower()
        if word not in stopwords.words('english') and len(word)>1:
            total_tokens2.append(word)

    counted_1 = Counter(total_tokens2).most_common()[:15]
    counted_2 = Counter(ngrams(total_tokens2, 2)).most_common()[:15]

    bigrams = []

    for i, j in counted_2:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        bigrams.append(temp2)

    counted_3 = Counter(ngrams(total_tokens2, 3)).most_common()[:15]

    trigrams = []

    for i, j in counted_3:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        trigrams.append(temp2)
    

    return dict(counted_1), dict(bigrams), dict(trigrams)



def createcloud_search(keywords, res):
    collection = ''

    keyword_list = []
    for i in keywords:
        keyword_list.append(i.word)

    for i in res:
        collection += str(i['text_full'])

    total_tokens = word_tokenize(collection)
    total_tokens2 = []
    total_tokens3 = []
    for word in total_tokens:
        word = re.sub("[^\w\d'\s_-]+", '', word).strip()
        word = word.lower()
        if word not in stopwords.words('english') and word not in keyword_list and len(word)>1 and word not in blank_words:
            total_tokens2.append(word)

    for word in total_tokens:
        word = re.sub("[^\w\d'\s_-]+", '', word).strip()
        word = word.lower()
        if word not in stopwords.words('english') and len(word)>1:
            total_tokens2.append(word)

    counted_1 = Counter(total_tokens2).most_common()[:15]
    counted_2 = Counter(ngrams(total_tokens2, 2)).most_common()[:15]

    bigrams = []

    for i, j in counted_2:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        bigrams.append(temp2)

    counted_3 = Counter(ngrams(total_tokens2, 3)).most_common()[:15]

    trigrams = []

    for i, j in counted_3:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        trigrams.append(temp2)


    

    return dict(counted_1), dict(bigrams), dict(trigrams)