from PyQt5 import QtWidgets
import time
import win32com.client  # слушаем USB
from threading import Thread  # потоки для кейлогера

from newkeylog import logger, read_keylog, read_bad_words, read_bad_guys_bad_word, write_bad_guys_bad_word
from chek_time import read_bad_guys_bad_time, chek_timimg, message, write_bad_guys_time

from Adminmenu_img import Ui_Adminmenu
from Chooseoptionsform import Ui_Chooseoptionsform
from Entering import Ui_Entering
from Newuserform import Ui_Newuserform
from Newuserpass import Ui_Newpassform
from Listofusers import Ui_Listofusers
from Userspace_img import Ui_Userspace
#from Outputform import Ui_Outputform
from USBAccess import Ui_USBAccess
from Magicsquare import Ui_MagicSquare


# self.users[Имя_пользователя]:
# [0] - пароль
# [1] - время регистрации пароля
# [2] - длина пароля
# [3] - минимальное время существования пароля
# [4] - обязательность спец сиволов
# [5] - активность пользователя
# [6] - разрешённые устройства

def about():
    message('Created by student Danila Urvantsev')

def news_from_file(file_name, title):
    try:
        f = open(file_name, 'r')
        st = f.readline().rstrip().split(' ')
        f.close()
    except FileNotFoundError:
        f = open(file_name, 'w')
        f.close()
        st = []
    except ValueError:
        f = open(file_name, 'w')
        f.close()
        st = []
    except SyntaxError:
        f = open(file_name, 'w')
        f.close()
        st = []
    out_msg = str(title)
    for i in st:
        out_msg += (' ' + i + ';')
    return out_msg

def clear_file(file_name):
    f = open(file_name, 'w')
    f.close()

class Tokb(QtWidgets.QMainWindow):
    def __init__(self):
        super(Tokb, self).__init__()
        self.wind = Ui_Entering()
        self.initiation()
        self.wind.Enter.clicked.connect(self.entering)

    def initiation(self):
        self.tryes = 3
        self.wind.setupUi(self)
        try:
            self.readall()
        except FileNotFoundError:
            self.if_file_error()
            self.readall()
        except ValueError:
            self.if_file_error()
            self.readall()
        except SyntaxError:
            self.if_file_error()
            self.readall()
        # print("Вход " + str(self.users.items()))
        for self.user in self.users:
            if self.users[self.user][5]:
                self.wind.Userslist.addItem(self.user)

    def entering(self):
        if self.tryes != 1:
            if self.wind.Userslist.currentText() == "Admin" and \
                    self.users[self.wind.Userslist.currentText()][0] == self.wind.Passwordform.text():
                self.wind = Ui_Adminmenu_2()
                self.wind.show()
                self.close()

            elif self.users[self.wind.Userslist.currentText()][0] == self.wind.Passwordform.text():
                self.name = self.wind.Userslist.currentText()
                self.openuserspacedialog()
            else:
                message('Not correct pass, you have ' + str(self.tryes - 1) + ' tryes')
                self.tryes = self.tryes - 1
        else:
            message('A lot of not correct passwords. Good bye!')
            self.close()

    def openuserspacedialog(self):
        self.readall()
        self.writepotok('0')
        self.dialog = Ui_Userspace()
        self.dialog.setupUi(self)
        self.dialog.Username.setText(self.name)
        self.dialog.Exit.clicked.connect(self.exitbutton)
        self.dialog.ChangepassButton.clicked.connect(self.open_new_pass_form_dialog)
        self.checkingpass()
        self.cheking_bad_time()

        self.thread1 = Thread(target=logger)
        self.thread1.start()
        # Условие заверщения

        wmi = win32com.client.GetObject("winmgmts:")
        for objItem in wmi.InstancesOf("CIM_DiskDrive"):
            if objItem.Caption is not None and objItem.MediaType == "Removable Media":
                if objItem.PNPDeviceID not in self.users[self.name][6]:
                    self.message_to_admin()
                else:
                    pass

    def open_new_pass_form_dialog(self):
        self.dialognp = Ui_Newpassform()
        self.dialognp.setupUi(self)
        self.dialognp.Back.clicked.connect(self.backtouserspacedialog)
        self.dialognp.Newpasssubmit.clicked.connect(self.create_new_pass)

    def create_new_pass(self):
        self.old_pass = self.dialognp.Olduserpass.text()
        if self.old_pass == self.users[self.name][0]:
            self.new_pass = self.dialognp.Newuserpass.text()
            if time.time() - self.users[self.name][1] < self.users[self.name][3]:
                message('You mast wait ' + str(
                    self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
                self.backtouserspacedialog()
            elif self.new_pass[len(self.new_pass) - 1] == ' ':
                message('The space (" ") can\'t be used as a last symbol of pass')
            elif len(self.new_pass) > 25:
                message('Max len of all passwords in system is 25')
            elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
                message('Pass is so short, min length is ' + str(self.users[self.name][2]))
            elif self.users[self.name][4]:
                if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.new_pass) or \
                        set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.new_pass) or \
                        set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.new_pass) or \
                        set("1234567890").isdisjoint(self.new_pass):
                    message('You must use special symbols, numbers and letters of different registers')
                else:
                    self.users[self.name][0] = self.new_pass
                    self.users[self.name][1] = time.time()
                    self.write_all()
                    message('Successful new pass')
                    self.backtouserspacedialog()
            else:
                self.users[self.name][0] = self.new_pass
                self.users[self.name][1] = time.time()
                self.write_all()
                message('Successful new pass')
                self.backtouserspacedialog()
        else:
            message('Old pass is not correct')

    def checkingpass(self):
        if self.users[self.name][4]:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
                    set("1234567890").isdisjoint(self.users[self.name][0]):
                message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.open_new_pass_form_dialog()
        if len(self.users[self.name][0]) < self.users[self.name][2]:
            message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
            self.open_new_pass_form_dialog()

    def readall(self):
        self.users = {}
        self.f = open('users.txt', 'r')
        self.users = dict(eval(self.f.readline().rstrip()))
        self.key = list(eval(self.f.readline().rstrip()))
        self.f.close()
        for user in self.users:
            self.users[user][0] = self.deshifr(self.users[user][0])
        if len(self.users) < 1:
            self.if_file_error()
        # print(self.users.items())
        # print(self.key)

    def if_file_error(self):
        self.users = {'Admin': ['Admin', time.time(), 1, 5, False, True, []]}
        self.key = [25, 13, 1, 19, 7, 16, 9, 22, 15, 3, 12, 5, 18, 6, 24, 8, 21, 14, 2, 20, 4, 17, 10, 23, 11]
        self.write_all()

    def writepotok(self, to_do):
        f = open('potok.txt', 'w')
        f.write(to_do)
        f.close()

    def write_all(self):
        for user in self.users:
            self.users[user][0] = self.shifr(self.users[user][0])
        self.f = open('users.txt', 'w')
        self.f.write(str(self.users))
        self.f.write('\n')
        self.f.write(str(self.key))
        self.f.close()
        for user in self.users:
            self.users[user][0] = self.deshifr(self.users[user][0])

    def backtouserspacedialog(self):
        if self.name != 'Admin':
            self.openuserspacedialog()

    def exitbutton(self):
        self.wind = Ui_Entering()
        self.writepotok('1')
        self.cheking_bad_word()
        self.cheking_bad_time()
        f = open('keylog.txt', 'w')
        f.close()
        #  self.thread1.join()
        self.initiation()
        self.wind.Enter.clicked.connect(self.entering)

    def message_to_admin(self):
        if self.name not in self.users['Admin'][6]:
            self.users['Admin'][6].append(self.name)
            self.write_all()

    def shifr(self, needs):
        new = ""
        for i in range(len(self.key)):
            if len(needs) < self.key[i]:
                new = new + " "
            else:
                new = new + needs[self.key[i] - 1]
        return new

    def deshifr(self, needs):
        new = ""
        for i in range(1, len(self.key) + 1):
            new = new + needs[self.key.index(i)]
        while new[len(new) - 1] == " ":
            new = new[0:len(new) - 1]
        return new

    def cheking_bad_word(self):
        words = read_keylog()
        bad_words = read_bad_words()
        bad_guys = read_bad_guys_bad_word()
        if bad_words == ['']:
            write_bad_guys_bad_word(bad_guys)
            return
        for i in bad_words:
            if i in words:
                if self.name not in bad_guys:
                    bad_guys.append(str(self.name))
        write_bad_guys_bad_word(bad_guys)

    def cheking_bad_time(self):
        bad_guys = read_bad_guys_bad_time()
        if not chek_timimg():
            if self.name not in bad_guys:
                bad_guys.append(str(self.name))
        write_bad_guys_time(bad_guys)


class Ui_Adminmenu_2(Tokb):
    def __init__(self):
        super(Ui_Adminmenu_2, self).__init__()
        self.admin = Ui_Adminmenu()
        self.initiationad()

    def initiationad(self):
        self.name = 'Admin'
        self.user = 'Admin'
        print(str(self.users.items()))
        self.readall()
        self.admin.setupUi(self)  # Инициализация GUI
        self.admin.NewuserButton.clicked.connect(self.opennewuserformdialog)  # Кнопка New user
        self.admin.ListofusersButton.clicked.connect(self.openlistofusersdialog)  # Кнопка List of users
        self.admin.ChangepassButton.clicked.connect(self.open_new_pass_form_dialog_ad)  # Кнопка Change pass
        self.admin.MagicsquareButton.clicked.connect(self.openmagicsquaredialogad)
        self.admin.ChooseoptionsButton.clicked.connect(self.openchooseoptionsformdialog)  # Кнопка Choose options
        self.admin.AboutButton.clicked.connect(about)
        self.admin.Exit.clicked.connect(self.openexitdialog)  # Кнопка Exit
        self.checking_pass_ad()
        self.bad_news()
        self.readall()

    # дублируем функции пароля для админа чтобы исключить баг мгновенного подтверждения пароля без ожидания времени

    def checking_pass_ad(self):
        if self.users[self.name][4]:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
                    set("1234567890").isdisjoint(self.users[self.name][0]):
                message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.open_new_pass_form_dialog_ad()
        if len(self.users[self.name][0]) < self.users[self.name][2]:
            message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
            self.open_new_pass_form_dialog_ad()

    def open_new_pass_form_dialog_ad(self):
        self.dialognp = Ui_Newpassform()
        self.dialognp.setupUi(self)
        self.dialognp.Back.clicked.connect(self.back_button)
        self.dialognp.Newpasssubmit.clicked.connect(self.create_new_pass_ad)

    def create_new_pass_ad(self):
        self.old_pass = self.dialognp.Olduserpass.text()
        if self.old_pass == self.users[self.name][0]:
            self.new_pass = self.dialognp.Newuserpass.text()
            if time.time() - self.users[self.name][1] < self.users[self.name][3]:
                message('You mast wait ' + str(
                    self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
                self.back_button()
            elif self.new_pass[len(self.new_pass) - 1] == ' ':
                message('The space (" ") can\'t be used as a last symbol of pass')
            elif len(self.new_pass) > 25:
                message('Max len of all passwords in system is 25')
            elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
                message('Pass is so short, min length is ' + str(self.users[self.name][2]))
            elif self.users[self.name][4]:
                if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.new_pass) or \
                        set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.new_pass) or \
                        set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.new_pass) or \
                        set("1234567890").isdisjoint(self.new_pass):
                    message('You must use special symbols, numbers and letters of different registers')
                else:
                    self.users[self.name][0] = self.new_pass
                    self.users[self.name][1] = time.time()
                    self.write_all()
                    message('Successful new pass')
                    self.back_button()
            else:
                self.users[self.name][0] = self.new_pass
                self.users[self.name][1] = time.time()
                self.write_all()
                message('Successful new pass')
                self.back_button()
        else:
            message('Old pass is not correct')

    def opennewuserformdialog(self):
        self.dialognu = Ui_Newuserform()
        self.dialognu.setupUi(self)
        self.dialognu.Back.clicked.connect(self.back_button)
        self.dialognu.Newusersubmit.clicked.connect(self.newusersubmit)

    def newusersubmit(self):
        if self.dialognu.Newusername.text() in self.users:
            message('You are already have this user')
        elif self.dialognu.Newusername.text() == '':
            message('The field is empty')
        elif self.dialognu.Newusername.text().isspace():
            message('The field is only spaces')
        else:
            self.users.update({self.dialognu.Newusername.text(): ["Qwerty1", time.time(), 1, 5, False, True, []]})
            self.write_all()
            message('User \"' + self.dialognu.Newusername.text() + '\" is created')
            self.back_button()

    def openlistofusersdialog(self):
        self.readall()
        self.ables = {}
        self.dialog = Ui_Listofusers()
        self.dialog.setupUi(self)
        r = 0
        for self.user in self.users:
            if self.user == 'Admin':
                pass
            else:
                if self.users[self.user][5]:
                    self.dialog.Userslist.addItem(self.user)
                else:
                    self.dialog.Userslist.addItem(self.user + ' (Disabled)')
                self.ables.update({r: self.user})
                r = r + 1
        self.dialog.deleteuserButton.clicked.connect(self.deletinguser)
        self.dialog.Options.clicked.connect(self.usersoptions)
        self.dialog.Back.clicked.connect(self.back_button)
        self.dialog.USB.clicked.connect(self.usbdialog)

    def usersoptions(self):
        if self.dialog.Userslist.count() < 1:
            message('List of users is empty')
        else:
            self.user = self.ables[self.dialog.Userslist.currentIndex()]
            self.openchooseoptionsformdialog()

    def usbdialog(self):
        if self.dialog.Userslist.count() < 1:
            message('List of users is empty')
        else:
            self.user = self.ables[self.dialog.Userslist.currentIndex()]
            self.user_usb = UsbAccess()
            r = 0
            self.able_usb = {}
            wmi = win32com.client.GetObject("winmgmts:")
            for objItem in wmi.InstancesOf("CIM_DiskDrive"):
                if objItem.Caption is not None and objItem.MediaType == "Removable Media":
                    if objItem.PNPDeviceID not in self.users[self.user][6]:
                        self.user_usb.wind.USBlist.addItem(objItem.Caption)
                    else:
                        self.user_usb.wind.USBlist.addItem("(✔)" + objItem.Caption)
                    self.able_usb.update({r: objItem})
                    r = r + 1

            self.user_usb.wind.Back.clicked.connect(self.usbclose)
            self.user_usb.wind.GiveaccessButton.clicked.connect(self.usb_access)
            self.user_usb.wind.DenyaccessButton.clicked.connect(self.usb_deny)
            self.user_usb.exec_()

    def usb_access(self):
        if self.user_usb.wind.USBlist.count() < 1:
            message('List of users is empty')
        else:
            self.selected_usb = self.able_usb[self.user_usb.wind.USBlist.currentIndex()]
            if self.selected_usb.PNPDeviceID not in self.users[self.user][6]:
                self.users[self.user][6].append(self.selected_usb.PNPDeviceID)
                self.write_all()
                self.usbclose()
                self.usbdialog()

    def usb_deny(self):
        if self.user_usb.wind.USBlist.count() < 1:
            message('List of users is empty')
        else:
            self.selected_usb = self.able_usb[self.user_usb.wind.USBlist.currentIndex()]
            if self.selected_usb.PNPDeviceID in self.users[self.user][6]:
                self.users[self.user][6].pop(self.users[self.user][6].index(self.selected_usb.PNPDeviceID))
                self.write_all()
                self.usbclose()
                self.usbdialog()

    def usbclose(self):
        self.user_usb.close()

    def deletinguser(self):
        if self.dialog.Userslist.count() < 1:
            message('List of users is empty')
        else:
            self.user = self.ables[self.dialog.Userslist.currentIndex()]
            if self.user == 'Admin':
                message('Admin can\'t be deleted!')
            else:
                self.users.pop(self.user)
                self.write_all()
                message('User \"' + self.user + '\" deleted')
                self.openlistofusersdialog()

    def openmagicsquaredialogad(self):
        self.dialogms = Ui_MagicSquare()
        self.dialogms.setupUi(self)
        for i in range(1, 26):
            nn = 'No_' + str(i)
            exec("self.dialogms." + nn + ".setValue(self.key[" + str(i - 1) + "])")
        self.dialogms.Submit.clicked.connect(self.submitms)

    def submitms(self):
        sumleft = self.dialogms.No_1.value() + self.dialogms.No_7.value() + self.dialogms.No_13.value() + self.dialogms.No_19.value() + self.dialogms.No_25.value()
        sumright = self.dialogms.No_5.value() + self.dialogms.No_9.value() + self.dialogms.No_13.value() + self.dialogms.No_17.value() + self.dialogms.No_21.value()
        stroks = [0, 0, 0, 0, 0]
        stolbs = [0, 0, 0, 0, 0]
        vr2 = 1
        for i in range(5):
            for j in range(5):
                nn = 'No_' + str(vr2)
                vr2 = vr2 + 1
                exec("stroks[" + str(i) + "] = stroks[" + str(i) + "] + self.dialogms." + nn + ".value()")
        vr2 = 1
        for i in range(5):
            for j in range(5):
                nn = 'No_' + str(vr2)
                vr2 = vr2 + 5
                exec("stolbs[" + str(i) + "] = stolbs[" + str(i) + "] + self.dialogms." + nn + ".value()")
            vr2 = (vr2 % 25) + 1
        fin = True
        for i in stroks:
            if i != 65:
                fin = False
        for i in stolbs:
            if i != 65:
                fin = False
        if (sumleft != 65) or (sumright != 65):
            fin = False
        vr2 = []
        for i in range(1, 26):
            nn = 'No_' + str(i)
            exec("vr2.append(self.dialogms." + nn + ".value())")
        vr = set(vr2)
        if len(vr2) != len(vr):
            fin = False
        if fin:
            for i in range(1, 26):
                nn = 'No_' + str(i)
                exec("self.key[" + str(i - 1) + "] = self.dialogms." + nn + ".value()")
            self.write_all()
            self.back_button()
        else:
            print('It\'s not magic square')

    def openchooseoptionsformdialog(self):
        self.dialogop = Ui_Chooseoptionsform()
        self.dialogop.setupUi(self)
        self.dialogop.Mindlin.setValue(self.users[self.user][2])
        self.dialogop.Mindlin.setMaximum(25)
        self.dialogop.Mintime.setValue(self.users[self.user][3])
        self.dialogop.checsimvol.setChecked(self.users[self.user][4])
        self.dialogop.Submit.clicked.connect(self.submitoptions)
        self.dialogop.Activate.clicked.connect(self.activation)
        self.dialogop.Deactivate.clicked.connect(self.deactivation)

    def activation(self):
        self.users[self.user][5] = True
        self.write_all()
        self.back_button()

    def deactivation(self):
        if self.user == 'Admin':
            message('Admin can\'t be deactivated!')
        else:
            self.users[self.user][5] = False
            self.write_all()
        self.back_button()

    def submitoptions(self):
        self.users[self.user][2] = self.dialogop.Mindlin.value()
        self.users[self.user][3] = self.dialogop.Mintime.value()
        self.users[self.user][4] = self.dialogop.checsimvol.isChecked()
        self.write_all()
        self.back_button()

    def openexitdialog(self):
        self.admin = Tokb()
        self.admin.show()
        self.close()

    def back_button(self):
        self.initiationad()

    def bad_news(self):
        all_bad_news = ''
        bad_guys_usb = 'Tried get access to the USB '
        if len(self.users[self.user][6]) != 0:
            for i in self.users[self.user][6]:
                bad_guys_usb += (' ' + i)

        bad_guys_words = news_from_file('bad_guys_bad_word.txt', '\nWrote bad words:')
        bad_guys_times = news_from_file('bad_guys_bad_time.txt', '\nTried to work not in time:')

        all_bad_news = bad_guys_usb + bad_guys_words + bad_guys_times

        message(all_bad_news)

        self.users[self.user][6] = []
        self.write_all()
        clear_file('bad_guys_bad_word.txt')
        clear_file('bad_guys_bad_time.txt')

class UsbAccess(QtWidgets.QDialog):
    def __init__(self):
        super(UsbAccess, self).__init__()
        self.wind = Ui_USBAccess()
        self.wind.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Tokb()
    window.show()
    app.exec_()
