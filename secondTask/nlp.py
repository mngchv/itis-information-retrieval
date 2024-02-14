# import spacy
# from bs4 import BeautifulSoup
# import re
# from collections import defaultdict
#
# # Загрузка модели для русского языка
# nlp = spacy.load("ru_core_news_sm")
#
# # Функция для токенизации текста
# def tokenize_text(text):
#     tokens = re.findall(r'\b\w+\b', text)
#     return tokens
#
# # Функция для фильтрации токенов
# def filter_tokens(tokens):
#     filtered_tokens = set()
#     stopwords = set(['и', 'в', 'на', 'с', 'по', 'о', 'а', 'не', 'или', 'что', 'как'])
#
#     for token in tokens:
#         if token.isalpha() and token not in stopwords and not any(char.isdigit() for char in token):
#             filtered_tokens.add(token.lower())
#
#     return filtered_tokens
#
# # Функция для лемматизации токенов
# def lemmatize_tokens(tokens):
#     lemmatized_tokens = defaultdict(list)
#
#     for token in tokens:
#         doc = nlp(token)
#         lemma = doc[0].lemma_ if doc else token
#         lemmatized_tokens[lemma].append(token)
#
#     return lemmatized_tokens
#
# # Чтение HTML-кода из файла
# with open('C:/Users/rming/PycharmProjects/pythonProject/firstTask/page_1.html', 'r', encoding='utf-8') as file:
#     html_content = file.read()
#
# # Используем BeautifulSoup для извлечения текста из HTML
# soup = BeautifulSoup(html_content, 'html.parser')
# text_content = soup.get_text()
#
# # Токенизация текста
# tokens = tokenize_text(text_content)
#
# # Фильтрация токенов
# filtered_tokens = filter_tokens(tokens)
#
# # Лемматизация токенов
# lemmatized_tokens = lemmatize_tokens(filtered_tokens)
#
# # Сохранение списка токенов в файл tokens.txt
# with open('tokens.txt', 'w', encoding='utf-8') as output_file:
#     for token in filtered_tokens:
#         output_file.write(token + '\n')
#
#
# # Сохранение группированных токенов в файл grouped_tokens.txt
# with open('grouped_tokens.txt', 'w', encoding='utf-8') as grouped_file:
#     for lemma, lemma_tokens in lemmatized_tokens.items():
#         grouped_file.write(f"{lemma} {' '.join(lemma_tokens)}\n")
import nltk.corpus
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from collections import defaultdict

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")

# Функция для токенизации текста
def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

# Функция для фильтрации токенов
def filter_tokens(tokens):
    filtered_tokens = set()
    stops = set(stopwords.words('russian'))

    for token in tokens:
        if token.isalpha() and token not in stops and not any(char.isdigit() for char in token):
            filtered_tokens.add(token.lower())

    return filtered_tokens

# Функция для лемматизации токенов
def lemmatize_tokens(tokens):
    lemmatized_tokens = defaultdict(list)

    for token in tokens:
        doc = nlp(token)
        lemma = doc[0].lemma_ if doc else token
        lemmatized_tokens[lemma].append(token)

    return lemmatized_tokens

# Открываем файлы для записи
with open('tokens.txt', 'w', encoding='utf-8') as tokens_file, \
     open('grouped_tokens.txt', 'w', encoding='utf-8') as grouped_file:

    # Цикл по всем файлам
    for i in range(1, 101):  # меняйте диапазон в соответствии с вашими файлами
        filename = f'C:/Users/rming/PycharmProjects/pythonProject/firstTask/page_{i}.html'

        # Чтение HTML-кода из файла
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Используем BeautifulSoup для извлечения текста из HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()

        # Токенизация текста
        tokens = tokenize_text(text_content)

        # Фильтрация токенов
        filtered_tokens = filter_tokens(tokens)

        # Лемматизация токенов
        lemmatized_tokens = lemmatize_tokens(filtered_tokens)

        # Запись в файл tokens.txt
        for token in filtered_tokens:
            tokens_file.write(token + '\n')

        # Запись в файл grouped_tokens.txt
        for lemma, lemma_tokens in lemmatized_tokens.items():
            grouped_file.write(f"{lemma} {' '.join(lemma_tokens)}\n")
