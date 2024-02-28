import spacy
import re
import nltk
import langdetect
import html2text
from nltk.corpus import stopwords
from collections import defaultdict

# Загружаем необходимые ресурсы nltk
nltk.download('punkt')
nltk.download('stopwords')

# Загружаем языковую модель spaCy
nlp = spacy.load("ru_core_news_sm")

# Инициализируем стоп-слова
stops = set(stopwords.words('russian'))

def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def filter_tokens(tokens):
    filtered_tokens = set()

    for token in tokens:
        # Дополнительные проверки для фильтрации "мусора"
        if (
            len(token) > 2 and  # Исключаем короткие слова
            token.isalpha() and
            token not in stops and
            not any(char.isdigit() for char in token) and
            token.lower() not in {'и', 'в', 'с', 'на', 'по', 'за', 'из', 'к', 'а', 'но', 'или', 'во', 'от'} and
            token.lower() not in {'см', 'также', 'nbsp', 'gt', 'lt', 'amp', 'raquo', 'laquo', 'mdash', 'ndash'} and
            langdetect.detect(token) == 'ru'  # Проверяем, является ли слово русским
        ):
            filtered_tokens.add(token.lower())

    return filtered_tokens


def lemmatize_tokens(tokens):
    lemmatized_tokens = defaultdict(list)

    for token in tokens:
        # Дополнительная проверка для исключения неправильно распарсенных слов
        if not any(char.isdigit() for char in token):
            doc = nlp(token)
            lemma = doc[0].lemma_ if doc else token
            lemmatized_tokens[lemma].append(token)

    return lemmatized_tokens

with open('tokens.txt', 'w', encoding='utf-8') as tokens_file, \
     open('grouped_tokens.txt', 'w', encoding='utf-8') as grouped_file:

    for i in range(1, 101):
        filename = f'/content/page_{i}.html'

        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Преобразуем HTML в чистый текст
        text_content = html2text.html2text(html_content)

        tokens = tokenize_text(text_content)

        filtered_tokens = filter_tokens(tokens)

        lemmatized_tokens = lemmatize_tokens(filtered_tokens)

        for token in filtered_tokens:
            tokens_file.write(token + '\n')

        for lemma, lemma_tokens in lemmatized_tokens.items():
            grouped_file.write(f"{lemma} {' '.join(lemma_tokens)}\n")
