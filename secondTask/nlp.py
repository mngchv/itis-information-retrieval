import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words("russian"))

lemmatizer = WordNetLemmatizer()


def extract_text_from_html(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text


def tokenize_and_lemmatize(text):
    tokens = word_tokenize(text)

    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]

    filtered_tokens = [token for token in lemmatized_tokens if token.isalpha() and token not in stop_words]

    return filtered_tokens


def process_document(html_file_path):
    text = extract_text_from_html(html_file_path)

    tokens = tokenize_and_lemmatize(text)

    return tokens


def save_tokens_to_file(tokens, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for token in tokens:
            file.write(token + '\n')


def save_lemmatized_tokens_to_file(lemmatized_tokens, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for lemmatized_token in lemmatized_tokens:
            file.write(lemmatized_token + '\n')


if __name__ == "__main__":

    html_file_path = 'C:/Users/rming/PycharmProjects/pythonProject/firstTask/page_1.html'

    tokens = process_document(html_file_path)

    save_tokens_to_file(tokens, 'tokens.txt')

    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    save_lemmatized_tokens_to_file(lemmatized_tokens, 'lemmatized_tokens.txt')
