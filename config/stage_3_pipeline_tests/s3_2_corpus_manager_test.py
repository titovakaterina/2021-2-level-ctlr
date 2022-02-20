import os
import json
import unittest

import pytest
import shutil

from core_utils.article import Article
from constants import ASSETS_PATH
from pipeline import CorpusManager, validate_dataset
from config.test_params import TEST_FILES_FOLDER


class ArticleInstanceCreationBasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_raw.txt"), os.path.join(ASSETS_PATH, "0_raw.txt"))

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_article_instance_is_created(self):
        try:
            self.assertIsInstance(self.corpus_manager.storage[0], Article, "CorpusManager does not initialize \
Article instance")
        except KeyError as exception:
            raise Exception("Corpus Manager does not create article instances when given raw files only") from exception

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_article_instance_fields_are_empty(self):

        article = self.corpus_manager.storage[0]
        self.assertFalse(any((article.title,
                              article.author,
                              article.topics,
                              article.date,
                              article.text)), "Newly created article instance fields must me empty\
unless there is meta file available")
        print(self.corpus_manager.storage)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(ASSETS_PATH, "0_raw.txt"))


class ArticleInstanceCreationAdvancedTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_meta.json"), os.path.join(ASSETS_PATH, "0_meta.json"))
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_raw.txt"), os.path.join(ASSETS_PATH, "0_raw.txt"))

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        with open(os.path.join(TEST_FILES_FOLDER, '0_meta.json'), encoding='utf-8') as f:
            self.meta = json.load(f)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_article_instance_is_created(self):
        try:
            _ = self.corpus_manager.storage[0]
        except KeyError:
            self.fail("Corpus Manager does not create article instances given both raw and meta files")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_article_instance_fields_are_filled(self):

        student_meta = self.corpus_manager.storage[0]._get_meta()

        message = '{field_name} field of newly created article instance differs from corresponding {field_name} \
value in meta file'

        self.assertEqual(student_meta.get('id'), self.meta.get('id'), message.format(field_name='Id'))
        self.assertEqual(student_meta.get('url'), self.meta.get('url'), message.format(field_name='URL'))
        self.assertEqual(student_meta.get('title'), self.meta.get('title'), message.format(field_name='title'))
        self.assertEqual(student_meta.get('author'), self.meta.get('author'), message.format(field_name='author'))
        self.assertEqual(student_meta.get('topics'), self.meta.get('topics'), message.format(field_name='topics'))

        self.assertFalse(student_meta.get('text'), 'Text field of newly created article instance must be empty')

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(ASSETS_PATH, "0_raw.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_meta.json"))
