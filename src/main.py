import re
import requests

from bs4 import BeautifulSoup
from fake_headers import Headers

    
def main():
    KEYWORDS = ['Умный', 'Математика', 'Хабр', 'Python']
    URL = "https://habr.com/ru/all/"

    headers = Headers(os="mac", headers=True).generate()
    resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    posts = soup.find_all('article', class_='tm-articles-list__item')

    for post in posts:
        href = post.find('h2', attrs={'data-test-id':'articleTitle'}).find('a').attrs.get('href')
        if post.find_all(string=[re.compile(keyword) for keyword in KEYWORDS]):
            date = post.find('time').attrs.get('title')
            title = post.find('h2', attrs={'data-test-id':'articleTitle'}).text
            print(f'<{date}> - <{title}> - <https://habr.com{href}>')
        else:
            article_url = f'https://habr.com{href}'
            article_resp = requests.get(url=article_url, headers=headers)
            article_soup = BeautifulSoup(article_resp.text, 'html.parser')
            article_body = article_soup.find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow")

            if article_body.find_all(string=[re.compile(keyword) for keyword in KEYWORDS]):
                date = post.find('time').attrs.get('title')
                title = post.find('h2', attrs={'data-test-id':'articleTitle'}).text
                print(f'<{date}> - <{title}> - <https://habr.com{href}>')

        
if __name__ == '__main__':
    main()
