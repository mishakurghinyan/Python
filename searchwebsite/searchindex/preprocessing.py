import string
# Preprocess text for searching


stop = open('searchindex/stopwords_en.txt').read().splitlines()


def preprocess_text(text:str) -> list[str]:
    """Preprocess the text for optimal search performance"""
    x = text.lower()
    new = x.translate(str.maketrans('', '', string.punctuation))
    newer = new.split(" ")
    final = []
    for i in newer:
        if i not in stop:
            final.append(i)

    # Currently no preprocessing implemented
    return final

