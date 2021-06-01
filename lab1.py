from PyQt5 import QtWidgets
import time
import win32com.client  # слушаем USB

from Adminmenu import Ui_Adminmenu
from Chooseoptionsform import Ui_Chooseoptionsform
from Entering import Ui_Entering
from Newuserform import Ui_Newuserform
from Newuserpass import Ui_Newpassform
from Listofusers import Ui_Listofusers
from Userspace import Ui_Userspace
from Outputform import Ui_Outputform


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
            self.f = open('users.txt', 'w')
            self.f.write("{'Admin':['Admin', ")
            self.f.write(str(time.time()))
            self.f.write(',')
            self.f.write('1, 5, False, True]}')
            self.f.close()
            self.readall()
        except ValueError:
            self.f = open('users.txt', 'w')
            self.f.write("{'Admin':['Admin', ")
            self.f.write(str(time.time()))
            self.f.write(',')
            self.f.write('1, 5, False, True]}')
            self.f.close()
            self.readall()

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
                self.message('Not correct pass, you have ' + str(self.tryes - 1) + ' tryes')
                self.tryes = self.tryes - 1
        else:
            self.message('A lot of not correct passwords. Good bye!')
            self.close()

    def openuserspacedialog(self):
        self.dialog = Ui_Userspace()
        self.dialog.setupUi(self)
        self.dialog.Username.setText(self.name)
        self.dialog.Exit.clicked.connect(self.exitbutton)
        self.dialog.ChangepassButton.clicked.connect(self.opennewpassformdialog)
        self.checkingpass()
        print(self.users.items())

    def opennewpassformdialog(self):
        self.dialognp = Ui_Newpassform()
        self.dialognp.setupUi(self)
        self.dialognp.Back.clicked.connect(self.backtouserspacedialog)
        self.dialognp.Newpasssubmit.clicked.connect(self.createnewpass)

    def createnewpass(self):
        self.oldpass = self.dialognp.Olduserpass.text()
        if self.oldpass == self.users[self.name][0]:
            self.newpass = self.dialognp.Newuserpass.text()
            if time.time() - self.users[self.name][1] < self.users[self.name][3]:
                self.message('You mast wait ' + str(
                    self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
                self.backtouserspacedialog()
            elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
                self.message('Pass is so short, min length is ' + str(self.users[self.name][2]))
            elif self.users[self.name][4]:
                if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
                        set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
                        set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
                        set("1234567890").isdisjoint(self.newpass):
                    self.message('You must use special symbols, numbers and letters of different registers')
                else:
                    self.users[self.name][0] = self.newpass
                    self.users[self.name][1] = time.time()
                    self.writeall()
                    self.message('Successful new pass')
                    self.backtouserspacedialog()
            else:
                self.users[self.name][0] = self.newpass
                self.users[self.name][1] = time.time()
                self.writeall()
                self.message('Successful new pass')
                self.backtouserspacedialog()
        else:
            self.message('Old pass is not correct')

    def checkingpass(self):
        if self.users[self.name][4]:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
                    set("1234567890").isdisjoint(self.users[self.name][0]):
                self.message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.opennewpassformdialog()
        if len(self.users[self.name][0]) < self.users[self.name][2]:
            self.message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
            self.opennewpassformdialog()

    def readall(self):
        self.users = {}
        self.f = open('users.txt', 'r')
        for line in self.f:
            self.users = dict(eval(line.rstrip()))
        self.f.close()
        if len(self.users) < 1:
            self.f = open('users.txt', 'w+')
            self.f.write("{'Admin':['Admin', ")
            self.f.write(str(time.time()))
            self.f.write(',')
            self.f.write('1, 5, False, True]}')
            self.f.close()
        print(self.users.items())

    def writeall(self):
        self.f = open('users.txt', 'w+')
        self.f.write(str(self.users))
        self.f.close()

    def backtouserspacedialog(self):
        if self.name != 'Admin':
            self.openuserspacedialog()

    def exitbutton(self):
        self.wind = Ui_Entering()
        self.initiation()
        self.wind.Enter.clicked.connect(self.entering)

    def message(self, needstext):
        error = Error()
        error.wind.textBrowser.setText(needstext)
        error.exec_()


class Ui_Adminmenu_2(Tokb):
    def __init__(self):
        super(Ui_Adminmenu_2, self).__init__()
        self.admin = Ui_Adminmenu()
        self.initiationad()

    def initiationad(self):
        self.name = 'Admin'
        self.user = 'Admin'
        self.readall()
        self.admin.setupUi(self)  # Инициализация GUI
        self.admin.NewuserButton.clicked.connect(self.opennewuserformdialog)  # Кнопка New user
        self.admin.ListofusersButton.clicked.connect(self.openlistofusersdialog)  # Кнопка List of users
        self.admin.ChangepassButton.clicked.connect(self.opennewpassformdialogad)  # Кнопка Change pass
        self.admin.ChooseoptionsButton.clicked.connect(self.openchooseoptionsformdialog)  # Кнопка Choose options
        self.admin.AboutButton.clicked.connect(self.about)
        self.admin.Exit.clicked.connect(self.openexitdialog)  # Кнопка Exit
        self.checkingpassad()

    # дублируем функции пароля для админа чтобы исключить баг мгновенного подтверждения пароля без ожидания времени

    def checkingpassad(self):
        if self.users[self.name][4]:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
                    set("1234567890").isdisjoint(self.users[self.name][0]):
                self.message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.opennewpassformdialogad()
        if len(self.users[self.name][0]) < self.users[self.name][2]:
            self.message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
            self.opennewpassformdialogad()

    def opennewpassformdialogad(self):
        self.dialognp = Ui_Newpassform()
        self.dialognp.setupUi(self)
        self.dialognp.Back.clicked.connect(self.backbutton)
        self.dialognp.Newpasssubmit.clicked.connect(self.createnewpassad)

    def createnewpassad(self):
        self.oldpass = self.dialognp.Olduserpass.text()
        if self.oldpass == self.users[self.name][0]:
            self.newpass = self.dialognp.Newuserpass.text()
            if time.time() - self.users[self.name][1] < self.users[self.name][3]:
                self.message('You mast wait ' + str(
                    self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
                self.backbutton()
            elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
                self.message('Pass is so short, min length is ' + str(self.users[self.name][2]))
            elif self.users[self.name][4]:
                if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
                        set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
                        set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
                        set("1234567890").isdisjoint(self.newpass):
                    self.message('You must use special symbols, numbers and letters of different registers')
                else:
                    self.users[self.name][0] = self.newpass
                    self.users[self.name][1] = time.time()
                    self.writeall()
                    self.message('Successful new pass')
                    self.backbutton()
            else:
                self.users[self.name][0] = self.newpass
                self.users[self.name][1] = time.time()
                self.writeall()
                self.message('Successful new pass')
                self.backbutton()
        else:
            self.message('Old pass is not correct')

    def opennewuserformdialog(self):
        self.dialognu = Ui_Newuserform()
        self.dialognu.setupUi(self)
        self.dialognu.Back.clicked.connect(self.backbutton)
        self.dialognu.Newusersubmit.clicked.connect(self.newusersubmit)

    def newusersubmit(self):
        if self.dialognu.Newusername.text() in self.users:
            self.message('You are already have this user')
        elif self.dialognu.Newusername.text() == '':
            self.message('The field is empty')
        elif self.dialognu.Newusername.text().isspace():
            self.message('The field is only spaces')
        else:
            self.users.update({self.dialognu.Newusername.text(): ["Qwerty1", time.time(), 1, 5, False, True]})
            self.writeall()
            self.message('User \"' + self.dialognu.Newusername.text() + '\" is created')
            self.backbutton()

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
        self.dialog.Back.clicked.connect(self.backbutton)

    def usersoptions(self):
        if self.dialog.Userslist.count() < 1:
            self.message('List of users is empty')
        else:
            # self.user = self.dialog.Userslist.currentText()
            self.user = self.ables[self.dialog.Userslist.currentIndex()]
            self.openchooseoptionsformdialog()

    def deletinguser(self):
        if self.dialog.Userslist.count() < 1:
            self.message('List of users is empty')
        else:
            self.user = self.ables[self.dialog.Userslist.currentIndex()]
            if self.user == 'Admin':
                self.message('Admin can\'t be deleted!')
            else:
                self.users.pop(self.user)
                self.writeall()
                self.message('User \"' + self.user + '\" deleted')
                self.openlistofusersdialog()

    def openchooseoptionsformdialog(self):
        self.dialogop = Ui_Chooseoptionsform()
        self.dialogop.setupUi(self)
        self.dialogop.Mindlin.setValue(self.users[self.user][2])
        self.dialogop.Mintime.setValue(self.users[self.user][3])
        self.dialogop.checsimvol.setChecked(self.users[self.user][4])
        self.dialogop.Submit.clicked.connect(self.submitoptions)
        self.dialogop.Activate.clicked.connect(self.activation)
        self.dialogop.Deactivate.clicked.connect(self.deactivation)

    def activation(self):
        self.users[self.user][5] = True
        self.writeall()
        self.backbutton()

    def deactivation(self):
        if self.user == 'Admin':
            self.message('Admin can\'t be deactivated!')
        else:
            self.users[self.user][5] = False
            self.writeall()
        self.backbutton()

    def submitoptions(self):
        self.users[self.user][2] = self.dialogop.Mindlin.value()
        self.users[self.user][3] = self.dialogop.Mintime.value()
        self.users[self.user][4] = self.dialogop.checsimvol.isChecked()
        self.writeall()
        self.backbutton()

    def about(self):
        self.message('Created by student Danila Urvantsev')

    def openexitdialog(self):
        self.admin = Tokb()
        self.admin.show()
        self.close()

    def backbutton(self):
        self.initiationad()


class Error(QtWidgets.QDialog):
    def __init__(self):
        super(Error, self).__init__()
        self.wind = Ui_Outputform()
        self.wind.setupUi(self)
        self.wind.textBrowser.setText('-*-')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Tokb()
    window.show()
    app.exec_()
