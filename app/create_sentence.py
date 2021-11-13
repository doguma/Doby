import en_core_web_sm
import re
import markovify
import warnings
warnings.filterwarnings('ignore')

# code here referenced from :
# https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33



def random_sentence(collection):

    nlp = en_core_web_sm.load()

    class POSifiedText(markovify.Text):
        def word_split(self, sentence):
            return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
        def word_join(self, words):
            sentence = ' '.join(word.split('::')[0] for word in words)
            return sentence

    gen2 = POSifiedText(collection, state_size=1)

    res_sent = gen2.make_short_sentence(max_chars=200)
    # res_sent = re.sub(' ,', ',', res_sent)
    # res_sent = re.sub(' .', '.', res_sent)
    # res_sent = re.sub(' - ', '-', res_sent)

    return res_sent