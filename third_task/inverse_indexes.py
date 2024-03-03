import json
import os
import os.path
import re
from collections import defaultdict

import langdetect
import spacy
from nltk.corpus import stopwords


def get_page_name(dir):
    return [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]


def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def filter_tokens(tokens):
    stops = set(stopwords.words('russian'))
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
    nlp = spacy.load("ru_core_news_sm")

    for token in tokens:
        # Дополнительная проверка для исключения неправильно распарсенных слов
        if not any(char.isdigit() for char in token):
            doc = nlp(token)
            lemma = doc[0].lemma_ if doc else token
            lemmatized_tokens[lemma].append(token)

    return lemmatized_tokens


if __name__ == '__main__':
    inverse_indexes = {}
    filePath = 'D:\\PycharmProjects\\itis-information-retrieval\\firstTask\\content'
    filenames = get_page_name(filePath)
    for filename in filenames:
        print(f'Filename = {filename}')
        with open(filePath + '/' + filename, 'r', encoding='utf_8_sig') as f:
            text = f.read()
        try:
            # Снова леммантизирую токены
            tokens = tokenize_text(text)
            filtered_tokens = filter_tokens(tokens)
            lemmatized_tokens = lemmatize_tokens(filtered_tokens)
        except Exception as e:
            print(e)
            continue
        for lemmatized_token in lemmatized_tokens:
            # Если нет в списке
            if lemmatized_token not in inverse_indexes:
                # То добавляю новый
                inverse_indexes[lemmatized_token] = [filename]
            else:
                # То добавляю в конец списка
                inverse_indexes[lemmatized_token].append(filename)
        print(f'Done part for filename = {filename}')
    with open('./inverted_indexes.json', 'w+', encoding='utf8') as stream:
        json.dump(inverse_indexes, stream, ensure_ascii=False)
    print('Done inversing indexes')
