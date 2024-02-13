import spacy
from bs4 import BeautifulSoup
import re

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")

# Функция для токенизации текста
def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

# Функция для фильтрации токенов
def filter_tokens(tokens):
    filtered_tokens = set()
    stopwords = set(['и', 'в', 'на', 'с', 'по', 'о', 'а', 'не', 'или', 'что', 'как'])

    for token in tokens:
        if token.isalpha() and token not in stopwords and not any(char.isdigit() for char in token):
            filtered_tokens.add(token.lower())

    return filtered_tokens

# Функция для лемматизации токенов
def lemmatize_tokens(tokens):
    lemmatized_tokens = {}

    for token in tokens:
        doc = nlp(token)
        lemma = doc[0].lemma_ if doc else token
        lemmatized_tokens[token] = lemma

    return lemmatized_tokens

# Чтение HTML-кода из файла
with open('C:/Users/rming/PycharmProjects/pythonProject/firstTask/page_1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Используем BeautifulSoup для извлечения текста из HTML
soup = BeautifulSoup(html_content, 'html.parser')
text_content = soup.get_text()

# Токенизация текста
tokens = tokenize_text(text_content)

# Фильтрация токенов
filtered_tokens = filter_tokens(tokens)

# Сохранение списка токенов в файл tokens.txt
with open('tokens.txt', 'w', encoding='utf-8') as output_file:
    for token in filtered_tokens:
        output_file.write(token + '\n')

# Лемматизация токенов
lemmatized_tokens = lemmatize_tokens(filtered_tokens)

# Сохранение лемматизированных токенов в файл lemmitized_tokens.txt
with open('lemmatized_tokens.txt', 'w', encoding='utf-8') as lemma_file:
    for token, lemma in lemmatized_tokens.items():
        lemma_file.write(f"{token}-{lemma}\n")
