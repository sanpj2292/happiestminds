
from .dictionary_thread import DictionaryThread
from .threads.word_thread import WordThread
from time import time
from math import floor, log10
import re

def get_flat_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def getWordData(word_list):
    first = [word_list[0]]
    unit_time = _calc_unit_time(first, WordThread)

    length = len(word_list)
    print(f'Word Length: {length}')
    n_threads = _calculateThreads(line_length=length,
                                  one_line_read_time=unit_time) + 1
    if n_threads > 400:
        n_threads = 400
    print(f'The number of threads: {n_threads}')
    ind_l = list(range(0, length, length // n_threads))
    print(f'Arg3: {length // n_threads}')
    w_threads = []
    for i in range(0, length):
        w_thread = WordThread(words=word_list[ind_l[i]:ind_l[i+1]])
        w_threads.append(w_thread)
        w_thread.start()
        if i == length - 1:
            w_thread = WordThread(words=word_list[ind_l[i]:])
            w_threads.append(w_thread)
            w_thread.start()
    for thread in w_threads:
        thread.join()
    return WordThread.words_details

def readFile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        gen = f.readlines()
        n_threads = 1
        n_lines = len(gen)
        thread_lines = []
        for i, line in enumerate(gen):
            if i == 0:
                n_threads = round(_calculateThreads(line_length=n_lines,
                                                    one_line_read_time=_calc_unit_time(line, DictionaryThread)) + 1)
                print(f'No of threads: {n_threads}')
                if n_threads > 40:
                    n_threads = 40
                thread_line = []
                thread_line.append(line)
                print(f'{n_lines//n_threads}')
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

        print(f'The length of thread_lines: { len(thread_lines) }')
        return DictionaryThread.line_words


def _calculateThreads(line_length, one_line_read_time):
    if one_line_read_time > 0 and one_line_read_time <= 1 :
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
        print(f'The value of v: {v}')
        return floor(line_length * one_line_read_time / int(v))
    else:
        return floor(line_length/80)

def _calc_unit_time(first_line, cls):
    r_thread = cls(first_line)
    st = time()
    r_thread.start()
    r_thread.join()
    en = time()
    print(f'Execution time for 1 line: {en-st}')
    return en - st
