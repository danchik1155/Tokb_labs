import time
from PyQt5 import QtWidgets

from Outputform import Ui_Outputform


def message(needs_text):
    error = Error()
    error.wind.textBrowser.setText(needs_text)
    error.exec_()


class Error(QtWidgets.QDialog):
    def __init__(self):
        super(Error, self).__init__()
        self.wind = Ui_Outputform()
        self.wind.setupUi(self)
        self.wind.textBrowser.setText('-*-')


def read_time():
    try:
        f = open('work_time.txt', 'r')
        st = f.readline().rstrip().split(' ')
        f.close()
        return st
    except FileNotFoundError:
        f = open('work_time.txt', 'w')
        f.write('7 23')
        f.close()
    except ValueError:
        f = open('work_time.txt', 'w')
        f.write('7 23')
        f.close()
    except SyntaxError:
        f = open('work_time.txt', 'w')
        f.write('7 23')
        f.close()
    return ['7', '23']

def read_bad_guys_bad_time():
    try:
        f = open('bad_guys_bad_time.txt', 'r')
        st = f.readline().rstrip().split(' ')
        f.close()
        return st
    except FileNotFoundError:
        f = open('bad_guys_bad_time.txt', 'w')
        f.close()
    except ValueError:
        f = open('bad_guys_bad_time.txt', 'w')
        f.close()
    except SyntaxError:
        f = open('bad_guys_bad_time.txt', 'w')
        f.close()
    return []


def write_bad_guys_time(bad_guys: list):
    bad_guys_str = ''
    for i in bad_guys:
        bad_guys_str += (i + ' ')
    f = open('bad_guys_bad_time.txt', 'w')
    f.write(bad_guys_str)
    f.close()


def cheking_borders(st):
    if len(st) != 2:
        error_in_time()
    new_st = list(st)
    for i in range(len(st)):
        new_st[i] = int(st[i])
    if new_st[0] >= new_st[1]:
        error_in_time()
    return new_st


def error_in_time():
    message('Please chek work_time.txt\nNot correct hours\nExamle:\n7 23')
    time.sleep(5)
    exit(0)


def chek_time(borders):
    now_time = time.localtime(time.time()).tm_hour
    if (now_time < borders[0]) or (now_time > borders[1]):
        return False
    return True


def chek_timimg():
    return chek_time(cheking_borders(read_time()))
