"""
Scrapper implementation
"""
import json
import os
import re

import requests


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
        pass

    def find_articles(self):
        """
        Finds articles
        """


    def get_search_urls(self):
        """
        Returns seed_urls param
        """
        pass


def prepare_environment(base_path):
    """
    Creates ASSETS_PATH folder if not created and removes existing folder
    """
    try:
        os.rmdir(base_path)
    except FileNotFoundError:
        pass
    finally:
        os.mkdir(base_path)


def validate_config(crawler_path):
    """
    Validates given config
    """
    with open(crawler_path) as file:
        config = json.load(file)
    max_articles = config["total_articles_to_find_and_parse"]
    seed_urls = config["seed_urls"]
    if not isinstance(max_articles, int):
        raise IncorrectNumberOfArticlesError
    if max_articles > 200:
        raise NumberOfArticlesOutOfRangeError
    part_of_string = re.compile(r'^https?://')
    for url in seed_urls:
        if not part_of_string.search(url):
            raise IncorrectURLError


if __name__ == '__main__':
    # YOUR CODE HERE
    pass
