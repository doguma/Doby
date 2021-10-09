from io import IncrementalNewlineDecoder
import numpy as np
import pandas as pd

from os import path
from PIL import Image

import matplotlib.pyplot as plt


def createcloud(res):
    collection = ''
    for i in res:
        collection += str(i['text'])

    # wordcloud = WordCloud().generate(text)

    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.savefig('/static/images/test_plot.png')