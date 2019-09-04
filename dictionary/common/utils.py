from dictionary import ALLOWED_EXTENSIONS
from dictionary.common.threads.dictionary_thread import DictionaryThread
from time import time
from math import floor
import re
from .database import Database
from pymongo.errors import BulkWriteError
from pymongo import InsertOne
from pprint import pprint
from PyDictionary import PyDictionary
from collections import namedtuple

"""
This namedtuple is an object that would be used to send data
to Flask View
"""
Dictionary = namedtuple('Dictionary', ['word', 'meanings', 'synonyms', 'antonyms'])


def allowed_file(filename: str) -> bool:
    """
    This methods validates if the filetype is indeed one of
    the types mentioned in the configuration parameter of Flask

    :param filename: str
    :return:  bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_flat_list(list_of_lists):
    """
    This method is used to flatten nested lists of order 1

    :type list_of_lists: list
    """
    return [item for sublist in list_of_lists for item in sublist]


def get_dictionary(search_word):
    """
    Gets the dictionary meaning of a word, it's antonym and synonym
    if available in the PyDictionary API

    :type search_word: str
    :return namedtuple|None
    """
    if Database.find_one(collection='words_list', query={'word': search_word}) is not None:
        mean = PyDictionary.meaning(search_word)
        syn = PyDictionary.synonym(search_word)
        ant = PyDictionary.antonym(search_word)
        return Dictionary(word=search_word, meanings=mean, synonyms=syn, antonyms=ant)
    else:
        return None


def insert_words(words_list: list) -> object:
    """
    Inserts the words from the uploaded text file into Database

    :param words_list: list
    :return: object
    """
    result = {}
    try:
        ops = []
        for op in words_list:
            if Database.find_one(collection='words_list', query={'word': op}) is None:
                ops.append(InsertOne({'word': op}))
        result = Database.bulk_write(collection='words_list', operations=ops)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    finally:
        return result


def readFile(filename: str) -> list:
    """
    Reads the file with a particular file name
    and gets words list from the file

    :param filename: str
    :return: list
    """
    with open(filename, 'r', encoding='utf-8') as f:
        gen = f.readlines()
        n_threads = 1
        n_lines = len(gen)
        thread_lines = []
        for i, line in enumerate(gen):
            if i == 0:
                unit_time = _calc_unit_time(line, DictionaryThread)
                n_threads = round(_calculateThreads(line_length=n_lines,
                                                    one_line_read_time=unit_time) + 1)
                if n_threads > 40:
                    n_threads = 40
                thread_line = [line]
                t_ind_list = list(range(0, n_lines, n_lines // n_threads))
                lookup_dict = {}
                for j in t_ind_list:
                    lookup_dict[j] = 1
            else:
                if lookup_dict.get(i) is not None:
                    thread_lines.append(thread_line)
                    thread_line = []
                else:
                    thread_line.append(line)

        if n_threads == 1:
            thread_lines.append(thread_line)

        threads = []
        for th_l in thread_lines:
            t = DictionaryThread(th_l)
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        return DictionaryThread.line_words


def _calculateThreads(line_length: int, one_line_read_time: float) -> int:
    """
    Calculates number of threads according to the length of string
    and the time taken to read one unit of a string

    :param line_length: int
    :param one_line_read_time: float
    :return: int
    """
    if 0 < one_line_read_time <= 1:
        return floor(line_length * one_line_read_time * 5)
    elif one_line_read_time > 1:
        l = str(one_line_read_time).split('.')
        if len(l[0]) > 1:
            v = '1' + '0' * len(l[0])
        else:
            if int(l[0]) > 0:
                v = '10'
            else:
                zeros = re.findall(r'^0{1,}', l[1])[0]
                if len(zeros) > 0:
                    v = '1' + re.findall(r'^0{1,}', l[1])[0]
                else:
                    v = '1'
        return floor(line_length * one_line_read_time / int(v))
    else:
        return floor(line_length / 80)


def _calc_unit_time(first_line, cls):
    """

    Parameters
    -------------
    first_one
     contains a unit string on which
     calculation of time is done to assist in calculation
     of number of threads required

    cls
     contains the class or Specifically Thread class
     which will be used for MultiThreading

    :type first_line: str
    :type cls: object

    :return float
    """
    r_thread = cls(first_line)
    st = time()
    r_thread.start()
    r_thread.join()
    en = time()
    return en - st
