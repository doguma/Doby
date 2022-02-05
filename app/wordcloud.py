import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter


blank_words = ['disease', 'background', 'reports', 'may', 'changes', 'report', 'suggested', 'exte', 'development', 'association', '\'s']


# create unigram, bigram, trigram for trending articles
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

    # unigram frequency
    counted_1 = Counter(total_tokens2).most_common()[:15]

    # bigram frequency
    counted_2 = Counter(ngrams(total_tokens2, 2)).most_common()[:15]

    bigrams = []

    for i, j in counted_2:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        bigrams.append(temp2)

    # trigram frequency
    counted_3 = Counter(ngrams(total_tokens2, 3)).most_common()[:15]

    trigrams = []

    for i, j in counted_3:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        trigrams.append(temp2)
    

    return dict(counted_1), dict(bigrams), dict(trigrams)



# create unigram, bigram, trigram for searched articles
def createcloud_search(keywords, res):
    collection = ''

    keyword_list = []
    for i in keywords:
        keyword_list.append(i.word)
    # do not include keyword itself

    for i in res:
        collection += str(i['text_full'])
    # concatenate full text

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

    # unigram
    counted_1 = Counter(total_tokens2).most_common()[:15]
    # bigram
    counted_2 = Counter(ngrams(total_tokens2, 2)).most_common()[:15]

    bigrams = []

    for i, j in counted_2:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        bigrams.append(temp2)

    # trigram
    counted_3 = Counter(ngrams(total_tokens2, 3)).most_common()[:15]

    trigrams = []

    for i, j in counted_3:
        temp2 = []
        temp2.append(' '.join(i))
        temp2.append(j)
        trigrams.append(temp2)

    return dict(counted_1), dict(bigrams), dict(trigrams)