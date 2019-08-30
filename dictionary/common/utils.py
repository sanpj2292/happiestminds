
from .dictionary_thread import DictionaryThread
from time import time
from math import floor


def readFile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        gen = f.readlines()
        n_threads = 1
        n_lines = len(gen)
        thread_lines = []
        for i, line in enumerate(gen):
            if i == 0:
                n_threads = round(_calculateThreads(line_length=n_lines,
                                                    one_line_read_time=_calc_unit_time(line)) + 1)
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

        print(DictionaryThread.line_words)

        print(f'The length of thread_lines: { len(thread_lines) }')
        return DictionaryThread.line_words


def _calculateThreads(line_length, one_line_read_time):
    if one_line_read_time > 0:
        return floor(line_length * one_line_read_time * 5)
    else:
        return floor(line_length/80)

def _calc_unit_time(first_line):
    r_thread = DictionaryThread(first_line)
    st = time()
    r_thread.start()
    r_thread.join()
    en = time()
    print(f'Execution time for 1 line: {en-st}')
    return en - st