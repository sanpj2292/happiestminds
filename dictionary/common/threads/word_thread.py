from . import Thread, Lock
from PyDictionary import PyDictionary
from collections import namedtuple

class WordThread(Thread):
    Dictionary = namedtuple('Dictionary', ['word','meanings', 'synonyms', 'antonyms'])
    words_details = []
    lock = Lock()

    def __init__(self, words):
        Thread.__init__(self)
        self.words = words

    def run(self):
        super(WordThread, self).run()
        details = []
        for word in self.words:
            w_inst = PyDictionary(word)
            detail = WordThread.Dictionary(
                word=word,
                meanings=w_inst.getMeanings(),
                synonyms=w_inst.getSynonyms(),
                antonyms=w_inst.getAntonyms())
            details.append(detail)
        self.lock.acquire()
        WordThread.words_details.append(details)
        self.lock.release()
