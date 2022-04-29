"""
Scrapper implementations
"""

import random
import json
import shutil
from time import sleep
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from constants import CRAWLER_CONFIG_PATH, ASSETS_PATH, HEADERS, HTTP_PATTERN
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
        part_urls = []
        all_urls_bs = article_bs.find_all('a', {"target": "_self"})
        for url_bs in all_urls_bs:
            url_to_article = url_bs['href']
            part_urls.append(url_to_article)
        full_urls = [HTTP_PATTERN + part_url for part_url in part_urls]

        for full_url in full_urls:
            if len(self.urls) < self.max_articles and full_url not in self.urls:
                self.urls.append(full_url)

        return full_urls

    def find_articles(self):
        """
        Finds articles
        """
        for seed_url in self.seed_urls:
            sleep(random.randint(1, 5))
            response = requests.get(url=seed_url, headers=HEADERS)
            if not response.ok:
                continue

            soup = BeautifulSoup(response.text, 'lxml')

            urls = self._extract_url(soup)
            for url in urls:
                if len(self.urls) < self.max_articles:
                    if url not in self.urls:
                        self.urls.append(url)


class HTMLParser:
    def __init__(self, article_url, article_id):
        self.article_url = article_url
        self.article_id = article_id
        self.article = Article(self.article_url, self.article_id)

    def _fill_article_with_meta_information(self, article_bs):
        self.article.author = 'NOT FOUND'

        try:
            topics_bs = article_bs.find_all('a', {'data-test': 'archive-record-header'})
            self.article.topics = [topic_bs.text for topic_bs in topics_bs]
        except AttributeError:
            self.article.topics = 'NOT FOUND'

        raw_date = str(article_bs.find('time', {'datetime': '2022-04-28T18:01:00'}))
        date = raw_date[:9]
        time = raw_date[11:15]
        complete_date = ', '.join([date, time])
        self.article.date = complete_date

        all_post_list_urls_bs = article_bs.find_all('a', {"target": "_self"})
        print(all_post_list_urls_bs)

    def _fill_article_with_text(self, article_bs):
        self.article.text = ''
        block_1 = article_bs.find('div', class_='_25BQZ')
        # text_1 = block_1.find('div')
        # text_11 = text_1.find('p')
        text_1 = block_1.find_all('p')
        for i in text_1:
            self.article.text += i.text

        # block_2 = article_bs.find('div', class_='_25BQZ')
        # text_2 = block_2.find('div')
        # text_2_2 = text_2.find('ul')
        # text_22 = text_2_2.find('li')
        # for k in text_22:
        #     self.article.text += k.text

    def parse(self):
        response = requests.get(url=self.article_url, headers=HEADERS)

        article_bs = BeautifulSoup(response.text, 'lxml')

        self._fill_article_with_text(article_bs)
        self._fill_article_with_meta_information(article_bs)
        return self.article


def prepare_environment(base_path):
    """
    Creates ASSETS_PATH folder if not created and removes existing folder
    """
    path_for_environment = Path(base_path)
    if path_for_environment.exists():
        shutil.rmtree(base_path)
    path_for_environment.mkdir(parents=True)


def validate_config(crawler_path):
    """
    Validates given config
    """
    with open(crawler_path) as file:
        configuration = json.load(file)

    if not configuration['seed_urls']:
        raise IncorrectURLError

    http_pattern = 'https://www.nn.ru/text/'
    for url in configuration["seed_urls"]:
        if http_pattern not in url:
            raise IncorrectURLError

    seed_urls = configuration["seed_urls"]
    total_articles_to_find_and_parse = configuration["total_articles_to_find_and_parse"]

    if not isinstance(total_articles_to_find_and_parse, int):
        raise IncorrectNumberOfArticlesError
    if total_articles_to_find_and_parse <= 0:
        raise IncorrectNumberOfArticlesError

    if total_articles_to_find_and_parse > 200:
        raise NumberOfArticlesOutOfRangeError

    return seed_urls, total_articles_to_find_and_parse


if __name__ == '__main__':
    seed_urls_main, total_articles_main = validate_config(CRAWLER_CONFIG_PATH)
    prepare_environment(ASSETS_PATH)

    crawler = Crawler(seed_urls_main, total_articles_main)
    crawler.find_articles()

    ID = 1
    for article_url_main in crawler.urls:
        article_parser = HTMLParser(article_url=article_url_main, article_id=ID)
        article = article_parser.parse()
        article.save_raw()
        ID += 1
