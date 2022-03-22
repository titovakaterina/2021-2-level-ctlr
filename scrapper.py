"""
Scrapper implementation
"""
from datetime import datetime
import json
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from constants import CRAWLER_CONFIG_PATH, ASSETS_PATH
from core_utils.article import Article


class IncorrectURLError(Exception):
    """
    Seed URL does not match standard pattern
    """


class NumberOfArticlesOutOfRangeError(Exception):
    """
    Total number of articles to parse is too big
    """


class IncorrectNumberOfArticlesError(Exception):
    """
    Total number of articles to parse in not integer
    """


class Crawler:
    """
    Crawler implementation
    """

    def __init__(self, seed_urls, max_articles: int):
        self.max_articles = max_articles
        self.seed_urls = seed_urls
        self.urls = []

    def _extract_url(self, article_bs):
        urls_bs = article_bs.find_all('a', class_='nohover')
        beginning_of_link = 'https://elementy.ru/'
        urls_bs_full = []
        for url_bs in urls_bs:
            not_full_link = url_bs['href']
            urls_bs_full.append(f'{beginning_of_link}{not_full_link}')

        for full_url in urls_bs_full:
            if len(self.urls) < self.max_articles and 'nauchno-populyarnaya_biblioteka' not in full_url:
                self.urls.append(full_url)

        return urls_bs_full

    def find_articles(self):
        """
        Finds articles
        """
        for seed_url in self.seed_urls:
            response = requests.get(url=seed_url)

            if not response.ok:
                continue

            soup = BeautifulSoup(response.text, 'lxml')

            self._extract_url(soup)

    def get_search_urls(self):
        """
        Returns seed_urls param
        """
        pass


class HTMLParser:
    def __init__(self, article_url, article_id):
        self.article_url = article_url
        self.article_id = article_id
        self.article = Article(article_url, article_id)

    def _fill_article_with_meta_information(self, article_bs):
        date = article_bs.find('span', class_='date')
        datetime_object = datetime.strptime(date.text, '%d.%m.%Y')
        self.article.date = datetime_object

        title = article_bs.find('h1')
        self.article.title = title.text

        sublink_bs = article_bs.find('div', class_='sublink')
        author_bs = sublink_bs.find('a')
        self.article.author = author_bs.text

        topics_bs = sublink_bs.find_all('a')[1]
        self.article.topics = topics_bs.text

    def _fill_article_with_text(self, article_bs):
        divs = article_bs.find('div', class_='memo')
        ps = divs.find_all('p')
        self.article.text = ''
        for p in ps:
            self.article.text += p.text

    def parse(self):
        response = requests.get(url=self.article_url)

        article_bs = BeautifulSoup(response.text, 'lxml')

        self._fill_article_with_text(article_bs)
        self._fill_article_with_meta_information(article_bs)

        return self.article


def prepare_environment(base_path):
    """
    Creates ASSETS_PATH folder if not created and removes existing folder
    """
    path = Path(base_path)
    if path.exists():
        shutil.rmtree(base_path)
    path.mkdir(parents=True, exist_ok=True)


def validate_config(crawler_path):
    """
    Validates given config
    """
    with open(crawler_path) as file:
        config = json.load(file)
    max_articles = config["total_articles_to_find_and_parse"]
    seed_urls = config["seed_urls"]
    if not seed_urls:
        raise IncorrectURLError

    if not isinstance(max_articles, int) or max_articles <= 0:
        raise IncorrectNumberOfArticlesError

    if max_articles > 200:
        raise NumberOfArticlesOutOfRangeError

    part_of_string = re.compile(r'^https?://')

    for url in seed_urls:
        if not part_of_string.search(url):
            raise IncorrectURLError
    return seed_urls, max_articles


if __name__ == '__main__':
    seed_urls_test, total_articles_test = validate_config(CRAWLER_CONFIG_PATH)
    prepare_environment(ASSETS_PATH)

    crawler = Crawler(seed_urls_test, total_articles_test)
    crawler.find_articles()

    ID = 0
    for article_url_test in crawler.urls:
        ID += 1
        article_parser = HTMLParser(article_url=article_url_test, article_id=ID)
        try:
            article = article_parser.parse()
            article.save_raw()
        except:
            print(article_parser.article.url)

