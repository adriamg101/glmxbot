import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    filtered = []
    for word in tokens:
        if word not in stopwords.words('english'):
            filtered.append(word.lower())
    return filtered