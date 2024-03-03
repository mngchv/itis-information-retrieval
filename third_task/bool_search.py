import json
import re


def load_index(file_name):
    with open(file_name, 'r', encoding='utf_8_sig') as f:
        return json.load(f)


def search(index, query):
    query = query.replace('(', ' ( ').replace(')', ' ) ')  # добавляем пробелы вокруг скобок для упрощения парсинга
    tokens = re.split(r'\s+', query)  # разбиваем запрос на токены
    return parse_expression(tokens, index)


def parse_expression(tokens, index):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            # находим соответствующую правую скобку
            depth = 1
            j = i + 1
            while depth > 0 and j < len(tokens):
                if tokens[j] == '(':
                    depth += 1
                elif tokens[j] == ')':
                    depth -= 1
                j += 1
            if j == len(tokens):
                raise ValueError('Не хватает правой скобки')
            sub_expression = tokens[i + 1:j]
            result = parse_expression(sub_expression, index)
            i = j
        elif token in {'AND', 'OR', 'NOT'}:
            if i == 0:
                raise ValueError('Ожидался операнд перед оператором')
            right = parse_operand(tokens[i + 1:], index)
            if token == 'AND':
                result = list(set(result) & set(right))
            elif token == 'OR':
                result = list(set(result) | set(right))
            elif token == 'NOT':
                result = list(set(index.keys()) - set(right))
                result = [page for page in result if page in index[query]]
            i += 2
        else:
            if i > 0 and tokens[i - 1] not in {'(', 'AND', 'OR', 'NOT'}:
                raise ValueError('Ожидался оператор перед операндом')
            result = parse_operand(tokens[i:], index)
            i += 1
        if i < len(tokens) and tokens[i] == ')':
            return result
    return result


def parse_operand(tokens, index):
    if len(tokens) == 0:
        raise ValueError('Ожидался операнд')
    term = tokens[0]
    if term in index:
        return index[term]
    else:
        return []


def sort_pages(pages):
    def extract_number(page):
        return int(page.split('_')[1].split('.')[0])

    return sorted(pages, key=extract_number)


index = load_index('inverted_indexes.json')
# Можно написать как соответствие AND регистр, так и (соответствие AND регистр) OR (фигура OR порядок)
query = input('Введите запрос: ')
results = search(index, query)
print('Результаты поиска:', sort_pages(results))
