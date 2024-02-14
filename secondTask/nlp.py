import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from collections import defaultdict

nlp = spacy.load("ru_core_news_sm")

def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def filter_tokens(tokens):
    filtered_tokens = set()
    stops = set(stopwords.words('russian'))

    for token in tokens:
        if token.isalpha() and token not in stops and not any(char.isdigit() for char in token):
            filtered_tokens.add(token.lower())

    return filtered_tokens

def lemmatize_tokens(tokens):
    lemmatized_tokens = defaultdict(list)

    for token in tokens:
        doc = nlp(token)
        lemma = doc[0].lemma_ if doc else token
        lemmatized_tokens[lemma].append(token)

    return lemmatized_tokens

with open('tokens.txt', 'w', encoding='utf-8') as tokens_file, \
     open('grouped_tokens.txt', 'w', encoding='utf-8') as grouped_file:

    for i in range(1, 101):
        filename = f'C:/Users/rming/PycharmProjects/pythonProject/firstTask/page_{i}.html'

        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()

        tokens = tokenize_text(text_content)

        filtered_tokens = filter_tokens(tokens)

        lemmatized_tokens = lemmatize_tokens(filtered_tokens)

        for token in filtered_tokens:
            tokens_file.write(token + '\n')

        for lemma, lemma_tokens in lemmatized_tokens.items():
            grouped_file.write(f"{lemma} {' '.join(lemma_tokens)}\n")
