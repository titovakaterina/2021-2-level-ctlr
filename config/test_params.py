import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
TEST_PATH = os.path.join(PROJECT_ROOT, 'test_tmp')
TEST_CRAWLER_CONFIG_PATH = os.path.join(TEST_PATH, 'crawler_config_test.json')
CRAWLER_CONFIG_PATH = os.path.join(PROJECT_ROOT, 'crawler_config.json')
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(CURRENT_DIR + "/../")
PARENT_CONFIG = os.path.join(PARENT_DIR, 'crawler_config.json')
TEST_FILES_FOLDER = os.path.join(PROJECT_ROOT, 'test_files')
PDF_ARTICLE_CONFIG = os.path.join(PROJECT_ROOT, 'test_files', 'crawler_config_separate_pdf.json')
