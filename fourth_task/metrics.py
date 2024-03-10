import re
from collections import Counter
from math import log10
import langdetect
from nltk.corpus import stopwords
import html2text
from os import listdir
import time

stops = set(stopwords.words('russian'))


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


def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def get_tf(pages_list, counters_list, word_in: set) -> list:
    pages_tf = []
    for page, counter in zip(pages_list, counters_list):
        count = len(page)
        tf = {}
        for word in word_in:
            tf[word] = counter[word] / count
        pages_tf.append(tf)
    return pages_tf


def get_idf(counters_list, count_of_pages: int, word_in: set) -> dict:
    counters = dict.fromkeys(word_in, 0)
    for p_counter in counters_list:
        for word in word_in:
            if p_counter[word] != 0:
                counters[word] += 1
    idf = {}
    for word in word_in:
        idf[word] = log10(count_of_pages / counters[word]) if counters[word] != 0 else 0
    return idf


def get_tf_idf(tf: list, idf: dict, word_in: set) -> list:
    idf_tf = []
    for tf_count in tf:
        idf_tf_dict = {}
        for word in word_in:
            idf_tf_dict[word] = tf_count[word] * idf[word]
        idf_tf.append(idf_tf_dict)
    return idf_tf


if __name__ == "__main__":
    content_file_path = 'D:\\PycharmProjects\\itis-information-retrieval\\firstTask\\content'
    tokens_file_path = 'D:\\PycharmProjects\\itis-information-retrieval\\secondTask\\tokens.txt'
    lemmas_file_path = 'D:\\PycharmProjects\\itis-information-retrieval\\secondTask\\lemms.txt'

    loaded_tokens = set()
    tokens_file = open(tokens_file_path, 'r', encoding='utf_8_sig')
    tokens_lines = tokens_file.readlines()

    for line in tokens_lines:
        loaded_tokens.add(line.strip())
    tokens_file.close()

    loaded_lemmas = set()
    lemmas_file = open(lemmas_file_path, 'r', encoding='utf_8_sig')
    lemmas_lines = lemmas_file.readlines()

    for line in lemmas_lines:
        loaded_lemmas.add(line.strip())
    lemmas_file.close()

    pages = []
    counters = []
    file_names = []
    for file_name in listdir(content_file_path):
        file = open(content_file_path + '/' + file_name, 'r', encoding='utf_8_sig')
        file_names.append(re.search('\\d+', file_name)[0])
        html_content = file.read()
        text_content = html2text.html2text(html_content)
        words_list = tokenize_text(text_content)
        tokens = []
        for word in words_list:
            if word in loaded_tokens:
                tokens.append(word)
        pages.append(tokens)
        counters.append(Counter(tokens))
        file.close()

    tokens_tf = get_tf(pages, counters, loaded_tokens)
    tokens_idf = get_idf(counters, len(pages), loaded_tokens)
    tokens_tf_idf = get_tf_idf(tokens_tf, tokens_idf, loaded_tokens)
    for page_tf_idf, file_name in zip(tokens_tf_idf, file_names):
        with open(f'D:\\PycharmProjects\\itis-information-retrieval\\fourth_task\\tf_idf_tokens\\{file_name}.txt', 'w',
                  encoding='utf_8_sig') as file:
            for word in loaded_tokens:
                file.write(f'{word} {tokens_idf[word]} {page_tf_idf[word]}\n')
    start = time.time()
    pages = []
    counters = []
    file_names = []
    for file_name in listdir(content_file_path):
        file = open(content_file_path + '/' + file_name, 'r', encoding='utf_8_sig')
        file_names.append(re.search('\\d+', file_name)[0])
        html_content = file.read()
        text_content = html2text.html2text(html_content)
        words_list = tokenize_text(text_content)
        filtered_tokens = filter_tokens(words_list)
        lemmas = []
        for word in filtered_tokens:
            if word in loaded_lemmas:
                lemmas.append(word)
        pages.append(lemmas)
        counters.append(Counter(lemmas))
        file.close()
    lemmas_tf = get_tf(pages, counters, loaded_lemmas)
    lemmas_idf = get_idf(counters, len(pages), loaded_lemmas)
    lemmas_tf_idf = get_tf_idf(lemmas_tf, lemmas_idf, loaded_lemmas)
    for page_tf_idf, file_name in zip(lemmas_tf_idf, file_names):
        with open(f'D:\\PycharmProjects\\itis-information-retrieval\\fourth_task\\tf_idf_lemmas\\{file_name}.txt', 'w',
                  encoding='utf_8_sig') as file:
            for word in loaded_lemmas:
                file.write(f'{word} {lemmas_idf[word]} {page_tf_idf[word]}\n')
    end = time.time() - start
    print(end)
