import re
import requests
import string
import os
from bs4 import BeautifulSoup

number_of_pages = int(input('Enter the number of pages: '))
type_of_article = input('Enter  the type of article: ')

for i in range(number_of_pages):
    folder_name = f'Page_{i + 1}'
    os.mkdir(folder_name)
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i + 1}'
    response = requests.get(url)

    if response.status_code == 200:
        articles_list_soup = BeautifulSoup(response.content, 'html.parser')
        articles = articles_list_soup.find_all('article')
        saved_links = []
        saved_articles = []

        for article in articles:
            if article.find('span', {"data-test": "article.type"}).text.strip() == type_of_article:
                saved_links.append(f'https://www.nature.com{article.a.get("href")}')

        for news_link in saved_links:
            news_article = requests.get(news_link)
            article_soup = BeautifulSoup(news_article.content, 'html.parser')
            title = article_soup.h1.text
            body = article_soup.find('div', class_=re.compile("body")).text

            for char in title:
                if char in string.punctuation:
                    title = title.replace(char, '')

            article_file_name = title.strip().split()
            article_file_name_formatted = '_'.join(article_file_name)

            article_file = open(f'{folder_name}/{article_file_name_formatted}.txt', 'wb')
            article_file.write(body.encode('utf8'))
            article_file.close()

            saved_articles.append(f'{article_file_name_formatted}.txt')

        print(f'Saved articles: [{", ".join(saved_articles)}] in folder {folder_name}')
    else:
        print(f'The URL returned {response.status_code}!')
