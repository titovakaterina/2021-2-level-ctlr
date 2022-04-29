"""
Pipeline for text processing implementation
"""


class EmptyDirectoryError(Exception):
    """
    No_data to process
    """


class InconsistentDatasetError(Exception):
    """
    Corrupt data:
        - numeration is expected to start from 1 and to be continuous
        - a number of text files must be equal to the number of meta files
        - text files must not be empty
    """


class MorphologicalToken:
    """
    Stores language params for each processed token
    """

    def __init__(self, original_word):
        pass

    def get_cleaned(self):
        """
        Returns lowercased original form of a token
        """
        pass

    def get_single_tagged(self):
        """
        Returns normalized lemma with MyStem tags
        """
        pass

    def get_multiple_tagged(self):
        """
        Returns normalized lemma with PyMorphy tags
        """
        pass


class CorpusManager:
    """
    Works with articles and stores them
    """

    def __init__(self, path_to_raw_txt_data: str):
        pass

    def _scan_dataset(self):
        """
        Register each dataset entry
        """
        pass

    def get_articles(self):
        """
        Returns storage params
        """
        pass


class TextProcessingPipeline:
    """
    Process articles from corpus manager
    """

    def __init__(self, corpus_manager: CorpusManager):
        pass

    def run(self):
        """
        Runs pipeline process scenario
        """
        pass

    def _process(self, raw_text: str):
        """
        Processes each token and creates MorphToken class instance
        """
        pass


def validate_dataset(path_to_validate):
    """
    Validates folder with assets
    """
    pass


from pymystem3 import Mystem
from pathlib import Path

def main():

    mystem = Mystem()
    file_path = Path(__file__).parent / 'seminars' / '04.15.2022' / 'test.txt'
    with file_path.open(encoding='utf-8') as file:
        plain_text = file.read()

    tokens = mystem.lemmatize(plain_text)
    clear = []
    pm = ['.', ',', '/', '!']
    for i in tokens:
        str_i = i.strip()
        if str_i in pm:
            if '' in i:
                clear.append(i)
            continue
        else:
            clear.append(i)

    for i in clear:
        ''.join(tokens)
    print(''.join(tokens))

    plain_text_analysis = mystem.analize(plain_text)\
    print(plain_text_analysis)

    count = 0

    for i in plain_text:
        if not i.get('analysis'):
            continue
        gr = i.get('analysis')[0].get('gr')
        if 'S,' in gr:
            print(gr)
            count+=1
    print(count)


        print ('word: ', i, gr)

import re

def mmain():
    name = 'Tom Gayler, 19 y.o.'
    p = re.compile(r'^[A-Z][a-z] \w+')
    p = re.compile(r'\w+ \w+, \d{1,3} y\.o\.')

    res=p.match(name)

    if res:
        print('String was matched')

    print(res.span())
    print(res.group())

    p=re.compile(r'\w+ \w+, \d{1,3} y\.o\.')
    res=p.match(name)

    print(res.group(0))
    print(res.group(1))
    print(res.group(2))
    print(res.group(3))

    file_path = Path(__file__).parent / 'seminars' / '04.22.2002' / 'logdata.txt'
    with open (file_path) as file:
        text = file.readlines()
    string = '146.204.224.152'
    pattern = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
    res = pattern.findall(text)
    print(len(res))

    with open(file_path) as file:
        text = file.readlines()
    headers_p = re.compile(r'POST|GET|PUT|DELETE')
    res = headers_p.findall(text)
    print(len(res))



    if __name__=='__main__':
        main()
