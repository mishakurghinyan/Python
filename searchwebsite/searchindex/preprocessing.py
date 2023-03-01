import string
import re
from nltk.stem import *

# Preprocess text for searching

stemmer = PorterStemmer()
stop = open('searchindex/stopwords_en.txt').read().splitlines()


def preprocess_text(text:str) -> list[str]:
    """Preprocess the text for optimal search performance"""
    lowered = text.lower()
    punctRem = lowered.translate(str.maketrans('', '', string.punctuation))
    splited = punctRem.split(" ")
    stopRem = []
    for i in splited:
        if i not in stop:
            stopRem.append(i)
            stemRem = []
    for x in stopRem:
        stemRem.append(stemmer.stem(x))
        # Currently no preprocessing implemented
    return stemRem

