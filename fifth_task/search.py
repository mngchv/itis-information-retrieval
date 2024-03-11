import re
import numpy as np
from os import listdir, path
from pymorphy3 import MorphAnalyzer
from scipy.spatial import distance


def get_links(file_path):
    readed_links = dict()
    with open(file_path, 'r', encoding='utf_8_sig') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split(': ')
            readed_links[key] = value
    return readed_links


def get_lemmas(directory):
    readed_lemmas = []
    file_names = listdir(directory)
    with open(directory + '/' + file_names[0], 'r', encoding='utf_8_sig') as file:
        lines = file.readlines()
        for line in lines:
            readed_lemmas.append(line.split(' ')[0])
    return readed_lemmas


def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def get_tf_idf(directory, lemmas_list):
    file_names = listdir(directory)
    zero_matrix = np.zeros((len(file_names), len(lemmas_list)))
    for file_name in file_names:
        file_number = int(re.search('\\d+', file_name)[0])
        with open(directory + '/' + file_name, 'r', encoding='utf_8_sig') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                lemma, idf, tf_idf = lines[i].split(' ')
                zero_matrix[file_number - 1][i] = float(tf_idf)
    return zero_matrix


def vectorize_query(query, lemmas_list, morph):
    vector = np.zeros(len(lemmas_list))
    tokens = tokenize_text(query)
    for token in tokens:
        parsed_token = morph.parse(token)[0]
        lemma = parsed_token.normal_form if parsed_token.normalized.is_known else token.lower()
        if lemma in lemmas_list:
            vector[lemmas_list.index(lemma)] = 1
    return vector


def search(query, links_list, lemmas_list, zero_matrix, morph):
    vector = vectorize_query(query, lemmas_list, morph)
    similarities = dict()
    document_index = 1
    for row in zero_matrix:
        dist = 1 - distance.cosine(vector, row)
        if dist > 0:
            similarities[document_index] = dist
        document_index += 1
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

    result = []
    for doc_index, score in sorted_similarities:
        if str(doc_index) in links_list:
            result.append(links_list[str(doc_index)])
        else:
            print(f"Ошибка: Документ под индексом {doc_index} не найден в ссылках.")
    return result


# nltk.download('punkt')
morph_analyzer = MorphAnalyzer()

index_file_path = path.dirname(__file__) + '/index.txt'
tf_idf_directory = path.dirname(__file__) + '/tf_idf_lemmas'

links = get_links(index_file_path)
lemmas = get_lemmas(tf_idf_directory)
matrix = get_tf_idf(tf_idf_directory, lemmas)


def vector_search(query):
    return search(query, links, lemmas, matrix, morph_analyzer)
