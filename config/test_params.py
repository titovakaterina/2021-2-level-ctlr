import os

TEST_SCRAPPER_CONFIG = 'scrapper_config_test.json'
SCRAPPER_CONFIG = 'scrapper_config.json'
SCRAPPER_CONFIG_PDF_PATH = 'scrapper_config_separate_pdf.json'

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
TEST_PATH = os.path.join(PROJECT_ROOT, 'test_tmp')

TEST_CRAWLER_CONFIG_PATH = os.path.join(TEST_PATH, TEST_SCRAPPER_CONFIG)
CRAWLER_CONFIG_PATH = os.path.join(PROJECT_ROOT, SCRAPPER_CONFIG)

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(CURRENT_DIR + "/../")
PARENT_CONFIG = os.path.join(PARENT_DIR, SCRAPPER_CONFIG)
TEST_FILES_FOLDER = os.path.join(PROJECT_ROOT, 'test_files')
PDF_ARTICLE_CONFIG = os.path.join(TEST_FILES_FOLDER, SCRAPPER_CONFIG_PDF_PATH)
