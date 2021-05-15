import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud


def get_text_from_pdf(pdfile) -> list:
    '''
    получение текста из pdf-документа.
    '''
    res = []

    with pdfplumber.open(pdfile) as pdf:
        for i in pdf.pages:
            res.append(i.extract_text())

    return res


def preprocessing_text(text: list) -> str:
    '''
    .
    '''
    clean_text = re.sub('[^A-Za-z]', ' ', ''.join(text).lower())  # перевели в нижний регист и оставили только слова

    nltk.download('punkt')
    tok_text = nltk.word_tokenize(clean_text)  # разбили на слова

    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    filter_text = [word for word in tok_text if
                   word not in stop_words and len(word) > 2]  # удалили все предлоги и слова меньше двух символов

    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    lemmatize_text = [lemmatizer.lemmatize(word) for word in filter_text]
    # print('Слова в начальной форме', '\n', lemmatize_text)

    return ' '.join(filter_text)


def get_tags(pdfile) -> str:
    text = get_text_from_pdf(pdfile)
    text = preprocessing_text(text)
    vectorizer = CountVectorizer(max_features=7)
    vectorizer.fit_transform([text])
    return ' '.join(vectorizer.get_feature_names())

