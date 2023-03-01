import string
import re
from nltk.stem import *

# Preprocess text for searching

stemmer = PorterStemmer()
stop = open('searchindex/stopwords_en.txt').read().splitlines()


def preprocess_text(text:str) -> list[str]:
    """Preprocess the text for optimal search performance"""
    tokens = text.lower()
    tokens = re.split('[^\w]', tokens)
    tokens = [word for word in tokens if word and word not in stop]
    tokens = [stemmer.stem(word) for word in tokens if word not in stop]
    return tokens

