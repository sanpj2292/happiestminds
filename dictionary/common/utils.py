
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


Dictionary = namedtuple('Dictionary', ['word', 'meanings', 'synonyms', 'antonyms'])

def get_flat_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def get_dictionary(search_word):
    if Database.find_one(collection='words_list', query={'word': search_word}) is not None:
        mean = PyDictionary.meaning(search_word)
        syn = PyDictionary.synonym(search_word)
        ant = PyDictionary.antonym(search_word)
        return Dictionary(word=search_word, meanings=mean, synonyms=syn, antonyms=ant)
    else:
        return None


def insert_words(words_list):
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


def readFile(filename):
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
                thread_line = []
                thread_line.append(line)
                t_ind_list = list(range(0, n_lines, n_lines//n_threads))
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


def _calculateThreads(line_length, one_line_read_time):
    if 0 < one_line_read_time <= 1:
        return floor(line_length * one_line_read_time * 5)
    elif one_line_read_time > 1:
        l = str(one_line_read_time).split('.')
        if len(l[0]) > 1:
           v = '1' + '0'*len(l[0])
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
        return floor(line_length/80)


def _calc_unit_time(first_line, cls):
    r_thread = cls(first_line)
    st = time()
    r_thread.start()
    r_thread.join()
    en = time()
    return en - st
