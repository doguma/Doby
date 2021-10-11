import re
import numpy as np
# import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter


blank_words = ['disease', 'background', 'reports', 'may', 'changes', 'report', 'suggested', 'exte', 'development', 'association', '\'s']

import random

class Markov(object):
	
	def __init__(self, words):
		self.cache = {}
		self.words = words
		self.word_size = len(self.words)
		self.database()
		
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 3):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in range(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.append(w2)
		return ''.join(gen_words)
			


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


    mark = Markov(collection)
    

    return dict(counted_1), dict(bigrams), dict(trigrams), mark.generate_markov_text()



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