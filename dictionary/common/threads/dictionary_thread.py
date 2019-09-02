from threading import Thread, Lock
import re

class DictionaryThread(Thread):
    line_words = set()
    lock = Lock()

    def __init__(self, read_lines):
        Thread.__init__(self)
        self.read_lines = read_lines

    def run(self):
        super(DictionaryThread, self).run()
        for line in self.read_lines:
            s_l = re.findall(r'[a-zA-Z\s]', line)
            words = ''.join(s_l).lstrip().split()
            DictionaryThread.lock.acquire()
            for word in words:
                DictionaryThread.line_words.add(word)
            DictionaryThread.lock.release()

