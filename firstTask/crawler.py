import requests

def download_page(url, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(response.text)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def crawl_pages_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]

    crawl_pages(urls)

def crawl_pages(urls):
    with open('index.txt', 'w', encoding='utf-8') as index_file:
        for i, url in enumerate(urls, 1):
            file_name = f"page_{i}.html"
            download_page(url, file_name)
            index_file.write(f"{i}: {url}\n")

if __name__ == "__main__":
    file_path = 'list.txt'

    crawl_pages_from_file(file_path)

