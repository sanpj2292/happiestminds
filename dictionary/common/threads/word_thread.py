from . import Thread, Lock

class WordThread(Thread):
    words_details = []
    lock = Lock()

    def __init__(self, words):
        Thread.__init__(self)
        self.words = words

    def run(self):
        pass