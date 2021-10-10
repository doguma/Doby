import numpy as np
# import pandas as pd



def createcloud(res):
    collection = ''
    for i in res:
        collection += str(i['text'])

    # wordcloud = WordCloud().generate(text)

    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.savefig('/static/images/test_plot.png')