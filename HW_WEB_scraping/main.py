import bs4
import requests

HEADERS= {
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/all'

def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features="html.parser")
    return soup


def get_link():
    links = []
    soup = get_soup(URL)
    articles = soup.find_all("article")
    for article in articles:
        link = article.find(class_="tm-article-snippet__readmore").attrs['href']
        links.append('https://habr.com' + link)
    return links


def get_info():
    links = get_link()
    count = 0
    for link in links:
        soup = get_soup(link)
        text = soup.find(class_="article-formatted-body").text
        for word in KEYWORDS:
            if word in text.strip():
                count += 1
                article = soup.find(class_="tm-article-snippet__title tm-article-snippet__title_h1").text
                date = soup.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"]
                print(f'{count}. Дата - {date}, название статьи - {article}, '
                      f'ссылка - {link}, содержит слово - {word}.')


if __name__ == '__main__':
    get_info()
