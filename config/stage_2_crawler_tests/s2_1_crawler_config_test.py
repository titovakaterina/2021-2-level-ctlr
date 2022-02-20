import json

import pytest

import scrapper
import unittest
from constants import CRAWLER_CONFIG_PATH
from config.test_params import TEST_PATH, TEST_CRAWLER_CONFIG_PATH
from scrapper import IncorrectURLError, IncorrectNumberOfArticlesError, NumberOfArticlesOutOfRangeError
from config.stage_2_crawler_tests.config_generator import generate_config


print("Stage 1A: Validating Crawler Config")
print("Starting tests with received config")


class ExtendedTestCase(unittest.TestCase):
    def assertRaisesWithMessage(self, msg, exception, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            print(msg)
            self.assertFail()
        except Exception as inst:
            self.assertEqual(type(inst), exception)


class CrawlerConfigCheck(ExtendedTestCase):
    def setUp(self) -> None:
        with open(CRAWLER_CONFIG_PATH) as f:
            self.reference = json.load(f)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_base_urls_config_param(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls=['plain text', 1],
                        num_articles=self.reference['total_articles_to_find_and_parse'])

        error_message = """Checking that scrapper can handle incorrect seed_urls inputs. 
                            If fails - Check URLs that you are trying to give to scrapper.
                            Some of them may not appear to be in the URL  format"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectURLError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_num_articles_config_param(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles=1000000)

        error_message = """Checking that num_articles parameter is not big for connection block.
                                If fails - Too big amount of articles to collect. 
                                Try less number of articles to collect"""
        self.assertRaisesWithMessage(error_message,
                                     NumberOfArticlesOutOfRangeError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_num_articles_config_param_type(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles='plain text')

        error_message = """Checking that number of articles parameter is integer.
                                If fails - check your config"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectNumberOfArticlesError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)


if __name__ == "__main__":
    unittest.main()
