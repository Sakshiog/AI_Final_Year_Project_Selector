import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

for pkg in ["stopwords", "wordnet", "omw-1.4"]:
    nltk.download(pkg, quiet=True)

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


class NLPProcessor:

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text):

        text = text.lower()

        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        words = text.split()

        words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word not in self.stop_words
        ]

        return " ".join(words)