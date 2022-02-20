import re
import os
import unittest

import pytest
import shutil

from constants import ASSETS_PATH
from pipeline import CorpusManager, TextProcessingPipeline, validate_dataset
from config.test_params import TEST_FILES_FOLDER


TAGS = ["A", "ADV", "S", "V", "PR", "ANUM"]


class ReferenceTextBasicPreprocessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_raw.txt"), os.path.join(ASSETS_PATH, "0_raw.txt"))
        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        with open(os.path.join(TEST_FILES_FOLDER, 'reference_score_four_test.txt'), 'r', encoding='utf-8') as rf:
            self.reference = rf.read()
        with open(os.path.join(ASSETS_PATH, "0_cleaned.txt"), "r", encoding='utf-8') as pr:
            self.processed = pr.read()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_reference_preprocessed_are_equal(self):
        # check number of tokens sequences
        self.assertEqual(len(self.reference.split()),
                         len(self.processed.split()),
                         msg=f"""Number of tokens sequences in reference {self.reference} 
                                                and processed {self.processed} texts is different""")

        # check tokenization
        self.assertEqual(self.reference.split(),
                         self.processed.split(),
                         msg="""Pipe does not tokenize admin text. Check how you tokenize""")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(ASSETS_PATH, "0_raw.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_cleaned.txt"))
        if os.path.exists(os.path.join(ASSETS_PATH, "0_single_tagged.txt")):
            os.remove(os.path.join(ASSETS_PATH, "0_single_tagged.txt"))
            if os.path.exists(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt")):
                os.remove(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt"))


class ReferenceTextAdvancedPreprocessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_meta.json"), os.path.join(ASSETS_PATH, "0_meta.json"))
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_raw.txt"), os.path.join(ASSETS_PATH, "0_raw.txt"))
        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        with open(os.path.join(TEST_FILES_FOLDER, 'reference_score_eight_test.txt'), 'r', encoding='utf-8') as rf:
            self.reference = rf.read()
        with open(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt"), "r", encoding='utf-8') as pr:
            self.processed = pr.read()
        self.re_pattern = r"\w+<*>\(*\)"

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_reference_preprocessed_are_equal(self):
        # check number of token word<tag> sequences
        self.assertEqual(len(self.reference.split()),
                         len(self.processed.split()),
                         msg=f"""Number of word<tag>(tag) sequences in reference {self.reference} 
                                                and processed {self.processed} texts is different""")

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_overall_format(self):
        # check correctness of word<tag> sequences
        for word_tag in self.processed.split():
            try:
                self.assertEqual(word_tag[-1], ")",
                                 msg=f"{word_tag} --- There should be ) at the end of each word<tag>(tag) sequence")
            except AssertionError:
                self.assertTrue(word_tag[-1].isalpha())
            try:
                self.assertTrue("<" in word_tag,
                                msg=f"{word_tag} --- < markup symbol should be in processed text")
            except AssertionError:
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"))
            try:
                self.assertTrue(word_tag[word_tag.index("<")-1].isalpha(),
                                msg=f"{word_tag} --- In tagged sequence there should be char symbol before < ")
            except ValueError:
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"))
            try:
                self.assertEqual(word_tag[word_tag.index(">")+1], "(",
                                 msg=f"{word_tag} --- There should be ( after > in the word<tag>(tag) sequence")
            except ValueError:
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"))

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_tag_format(self):
        # check TAGS ander each sequences:
        tags_pattern = r"<([A-Z]+)[,=]{1}"
        reference_tags = re.findall(tags_pattern, self.reference)
        processed_tags = re.findall(tags_pattern, self.processed)

        # check tag correctness.
        # Optional, but should be the same across each tagger, as reference example is too simple
        for tag in processed_tags:
            self.assertTrue(tag in TAGS,
                            msg=f"Tag {tag} is not known. Is it in required tags list?")
        self.assertEqual(reference_tags, processed_tags,
                         msg=f"""Tag sequence from reference text {reference_tags}
                                    differs from processed text {processed_tags}""")

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_pymorphy_tag_format(self):
        reference_tags = self.reference.split()
        processed_tags = self.processed.split()
        self.assertEqual(reference_tags, processed_tags,
                         msg=f"""Tag sequence from reference text {reference_tags}
                                            differs from processed text {processed_tags}""")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(ASSETS_PATH, "0_meta.json"))
        os.remove(os.path.join(ASSETS_PATH, "0_raw.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_cleaned.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_single_tagged.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt"))


class ReferenceTextMediumPreprocessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_meta.json"), os.path.join(ASSETS_PATH, "0_meta.json"))
        shutil.copyfile(os.path.join(TEST_FILES_FOLDER, "0_raw.txt"), os.path.join(ASSETS_PATH, "0_raw.txt"))
        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        with open(os.path.join(TEST_FILES_FOLDER, 'reference_test.txt'), 'r', encoding='utf-8') as rf:
            self.reference = rf.read()
        with open(os.path.join(ASSETS_PATH, "0_single_tagged.txt"), "r", encoding='utf-8') as pr:
            self.processed = pr.read()
        self.re_pattern = r"\w+<*>"

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_reference_preprocessed_are_equal(self):
        # check number of token word<tag> sequences
        self.assertEqual(len(re.findall(self.re_pattern, self.reference)),
                         len(re.findall(self.re_pattern, self.processed)),
                         msg=f"""Number of word<tag> sequences in reference {self.reference} 
                                                and processed {self.processed} texts is different""")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_overall_format(self):
        # check correctness of word<tag> sequences
        for word_tag in self.processed.split():
            self.assertEqual(word_tag[-1], ">",
                             msg=f"{word_tag} --- There should be > at the end of each word<tag> sequence")
            self.assertTrue("<" in word_tag,
                            msg=f"{word_tag} --- < markup symbol should be in processed text")
            self.assertTrue(word_tag[word_tag.index("<")-1].isalpha(),
                            msg=f"{word_tag} --- In tagged sequence there should be char symbol before < ")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_admin_data_processing
    def test_tag_format(self):
        # check TAGS ander each sequences:
        tags_pattern = r"<([A-Z]+)[,=]{1}"
        reference_tags = re.findall(tags_pattern, self.reference)
        processed_tags = re.findall(tags_pattern, self.processed)

        # check tag correctness.
        # Optional, but should be the same across each tagger, as reference example is too simple
        for tag in processed_tags:
            self.assertTrue(tag in TAGS,
                            msg=f"Tag {tag} is not known. Is it in required tags list?")
        self.assertEqual(reference_tags, processed_tags,
                         msg=f"""Tag sequence from reference text {reference_tags}
                                    differs from processed text {processed_tags}""")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(ASSETS_PATH, "0_meta.json"))
        os.remove(os.path.join(ASSETS_PATH, "0_raw.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_cleaned.txt"))
        os.remove(os.path.join(ASSETS_PATH, "0_single_tagged.txt"))
        if os.path.isfile(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt")):
            os.remove(os.path.join(ASSETS_PATH, "0_multiple_tagged.txt"))
