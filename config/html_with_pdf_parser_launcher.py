"""
Launcher for pages containing PDF articles
"""


import os
import ssl

from scrapper import PDFCrawler, HTMLWithPDFParser, PDFParser
from scrapper import validate_config, prepare_environment
from constants import PROJECT_ROOT, ASSETS_PATH


if __name__ == "__main__":
    # ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    # Validate config
    seed_urls_, max_articles_ = validate_config(os.path.join(
        PROJECT_ROOT, 'config', 'test_files', 'crawler_config_separate_pdf.json'))
    print(f'Need to find {max_articles_} articles')

    # Prepare environment
    prepare_environment(ASSETS_PATH)

    # Collect all articles
    crawler = PDFCrawler(seed_urls=seed_urls_, max_articles=max_articles_)
    crawler.find_articles()

    # Parse each article separately
    PAGE_ID = 1
    for i, article_url in enumerate(crawler.urls):
        if PAGE_ID >= max_articles_+1:
            break
        if article_url.endswith('.pdf'):
            print(f'Monolithic PDF Page {article_url}')
            parser = PDFParser(article_url, PAGE_ID)
            articles = parser.parse()
            for article in articles:
                if PAGE_ID < max_articles_+1:
                    article.save_raw()
                    PAGE_ID += 1
        else:
            print(f'Separate PDF Page {article_url}')
            parser = HTMLWithPDFParser(article_url, PAGE_ID)
            article = parser.parse()
            article.save_raw()
            PAGE_ID += 1
    print('Done')
