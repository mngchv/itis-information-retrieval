import requests


def get_category_members(category, limit=100):
    base_url = 'https://ru.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmlimit': limit,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'error' in data:
        print(f"Error: {data['error']['info']}")
        return []

    return [page['title'] for page in data['query']['categorymembers']]


def get_article_url(title):
    base_url = 'https://ru.wikipedia.org/wiki/'
    return base_url + title.replace(' ', '_')


if __name__ == "__main__":
    category_name = 'Гербы_по_алфавиту'
    limit = 100

    articles = get_category_members(category_name, limit)

with open('list.txt', 'w', encoding='utf-8') as file:
    for i, article in enumerate(articles, 1):
        url = get_article_url(article)
        file.write(f'{url} \n')
