import re
import os
import unittest

import pytest

from constants import ASSETS_PATH


TAGS = ["A", "ADV", "S", "V", "PR", "ANUM", "CONJ", "SPRO", "APRO", "PART", "NUM", "ADVPRO", "INTJ", "COM"]

PUNCTUATION_MARKS = [',', '.', '-', ';', ':', '!', '?', '<']


class StudentTextBasicPreprocessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.articles = dict()
        for article in os.listdir(ASSETS_PATH):
            if article.endswith("_cleaned.txt"):
                with open(os.path.join(ASSETS_PATH, article), "r", encoding="utf-8") as txt:
                    self.articles[int(article[:-12])] = txt.read()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_student_dataset_validation
    def test_tagging_format_tokens_format(self):
        for article_id, article_text in self.articles.items():
            for token in article_text.split():
                self.assertTrue(token not in PUNCTUATION_MARKS,
                                msg=f"""There are some punctuation marks found in article {article_id}""")
                self.assertTrue(token.islower(),
                                msg=f"""Token {token} in article {article_id} is not lowercased""")


class StudentTextAdvancedPreprocessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.articles = dict()
        for article in os.listdir(ASSETS_PATH):
            if article.endswith("_multiple_tagged.txt"):
                with open(os.path.join(ASSETS_PATH, article), "r", encoding="utf-8") as txt:
                    self.articles[int(article[:-20])] = txt.read()

    @staticmethod
    def custom_split(string) -> list:
        return [element+')' for element in string.split(') ')]

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_student_dataset_validation
    def test_tagging_format_tokens_format(self):
        for article_id, article_text in self.articles.items():
            word_tag_sequences = self.custom_split(article_text)
            print(word_tag_sequences)
            for sequence in word_tag_sequences:
                self.assertEqual(sequence[-1], ")",
                                 msg=f"{sequence} --- There should be > at the end of each word<tag> sequence")
                self.assertTrue("<" in sequence,
                                msg=f"{sequence} --- < markup symbol should be in processed text")
                self.assertTrue(sequence[sequence.index("<") - 1].isalpha(),
                                msg=f"{sequence} --- In tagged sequence there should be char symbol before < ")

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_student_dataset_validation
    def test_tags_correctness(self):
        for article_id, article_text in self.articles.items():
            tags = re.findall(r"<([A-Z]+)[,=]?", article_text)
            for tag in tags:
                self.assertTrue(tag in TAGS,
                                msg=f"""Tag {tag} not in list of known mystem tags""")


class StudentTextMediumPreprocessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.articles = dict()
        for article in os.listdir(ASSETS_PATH):
            if article.endswith("_single_tagged.txt"):
                with open(os.path.join(ASSETS_PATH, article), "r", encoding="utf-8") as txt:
                    self.articles[int(article[0])] = txt.read()

    @staticmethod
    def custom_split(string) -> list:
        return [element+'>' for element in string.split('>')][:-1]

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_student_dataset_validation
    def test_tagging_format_tokens_format(self):
        for article_id, article_text in self.articles.items():
            word_tag_sequences = self.custom_split(article_text)
            for sequence in word_tag_sequences:
                self.assertEqual(sequence[-1], ">",
                                 msg=f"{sequence} --- There should be > at the end of each word<tag> sequence")
                self.assertTrue("<" in sequence,
                                msg=f"{sequence} --- < markup symbol should be in processed text")
                self.assertTrue(sequence[sequence.index("<") - 1].isalpha(),
                                msg=f"{sequence} --- In tagged sequence there should be char symbol before < ")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_student_dataset_validation
    def test_tags_correctness(self):
        for article_id, article_text in self.articles.items():
            tags = re.findall(r"<([A-Z]+)[,=]?", article_text)
            for tag in tags:
                self.assertTrue(tag in TAGS,
                                msg=f"""Tag {tag} not in list of known mystem tags""")
