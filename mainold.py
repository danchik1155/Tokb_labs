from PyQt5 import QtWidgets
import time
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
        self.wind.setupUi(self)
        try:
            self.readparam()
        except FileNotFoundError:
            self.f = open('param.txt', 'w')
            self.f.write('1')
            self.f.write('\n')
            self.f.write('5')
            self.f.write('\n')
            self.f.write('0')
            self.f.close()
            self.readparam()
        except ValueError:
            self.f = open('param.txt', 'w')
            self.f.write('1')
            self.f.write('\n')
            self.f.write('5')
            self.f.write('\n')
            self.f.write('0')
            self.f.close()
            self.readparam()
        try:
            self.readusers()
        except FileNotFoundError:
            self.f = open('user.txt', 'w')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.close()
            self.readusers()
        try:
            self.readlastpass()
        except FileNotFoundError:
            self.f = open('lastpas.txt', 'w')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write(str(time.time()))
            self.f.write('\n')
            self.f.close()
            self.readlastpass()
        except ValueError:
            self.f = open('lastpas.txt', 'w')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write(str(time.time()))
            self.f.write('\n')
            self.f.close()
            self.readlastpass()

        for self.user in self.users:
            self.wind.Userslist.addItems([self.user])

    def entering(self):
        if self.wind.Userslist.currentText() == "Admin" and \
                self.users[self.wind.Userslist.currentText()] == self.wind.Passwordform.text():
            self.wind = Ui_Adminmenu_2()
            self.wind.show()
            self.close()

        elif self.users[self.wind.Userslist.currentText()] == self.wind.Passwordform.text():
            self.name = self.wind.Userslist.currentText()
            self.openuserspacedialog()

        else:
            self.message('Not correct pass')

    def openuserspacedialog(self):
        self.dialog = Ui_Userspace()
        self.dialog.setupUi(self)
        self.dialog.Username.setText(self.name)
        self.dialog.Exit.clicked.connect(self.exitbutton)
        self.dialog.ChangepassButton.clicked.connect(self.opennewpassformdialog)
        self.checkingpass()
        print(self.users.items())

    def opennewpassformdialog(self):
        self.dialog = Ui_Newpassform()
        self.dialog.setupUi(self)
        self.dialog.Back.clicked.connect(self.backtouserspacedialog)
        self.dialog.Newpasssubmit.clicked.connect(self.createnewpass)

    def createnewpass(self):
        self.newpass = self.dialog.Newuserpass.text()
        if time.time() - self.lasts[self.name][1] < self.mintime:
            self.message('You mast wait ' + str(int(time.time() - self.lasts[self.name][1])) + ' seconds')
        if len(self.dialog.Newuserpass.text()) < self.mindlin:
            self.message('Pass is so short, min length is ' + str(self.mindlin))
        elif self.spec:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
                    set("1234567890").isdisjoint(self.newpass):
                self.message('You must use special symbols, numbers and letters of different registers')
            else:
                self.users[self.name] = self.newpass
                self.user = ''
                self.writeusers()
                self.lasts[self.name][0] = self.newpass
                self.lasts[self.name][1] = time.time()
                self.writelastpass()
                self.message('Successful new pass')
                self.backtouserspacedialog()
        else:
            self.users[self.name] = self.newpass
            self.user = ''
            self.writeusers()
            self.lasts[self.name][0] = self.newpass
            self.lasts[self.name][1] = time.time()
            self.writelastpass()
            self.message('Successful new pass')
            self.backtouserspacedialog()

    def writeusers(self):
        self.f = open('user.txt', 'w+')
        for vrem in self.users:
            if vrem == self.user:
                pass
            else:
                self.f.write(vrem)
                self.f.write('\n')
                self.f.write(self.users[vrem])
                self.f.write('\n')
        self.f.close()

    def readusers(self):
        self.users = {}
        self.f = open('user.txt', 'r')
        l = 1
        r = 0
        names = ""
        for line in self.f:
            if l == 1:
                names = line.rstrip()
                l = 2
            else:
                y = {(names, line.rstrip('\n'))}
                self.users.update(y)
                l = 1
            r = r + 1
        self.f.close()
        if r < 2 or r % 2 != 0:
            self.f = open('user.txt', 'w')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.close()
        print(self.users.items())

    def readparam(self):
        self.f = open('param.txt', 'r')
        self.mindlin = int(self.f.readline().rstrip())
        self.mintime = int(self.f.readline().rstrip())
        if int(self.f.readline().rstrip()) == 0:
            self.spec = False
        else:
            self.spec = True
        self.f.close()
        print([self.mindlin, self.mintime, self.spec])

    def checkingpass(self):
        if self.spec:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name]) or \
                    set("1234567890").isdisjoint(self.users[self.name]):
                self.message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.opennewpassformdialog()
        if len(self.users[self.name]) < self.mindlin:
            self.message('Your pass is so short, min length is ' + str(self.mindlin))
            self.opennewpassformdialog()

    def writelastpass(self):
        self.f = open('lastpas.txt', 'w+')
        for vrem in self.lasts:
            if vrem == self.user:
                pass
            else:
                self.f.write(vrem)
                self.f.write('\n')
                self.f.write(self.lasts[vrem][0])
                self.f.write('\n')
                self.f.write(str(self.lasts[vrem][1]))
                self.f.write('\n')
        self.f.close()

    def readlastpass(self):
        self.lasts = {}
        self.f = open('lastpas.txt', 'r')
        l = 1
        r = 0
        names = ""
        for line in self.f:
            if l == 1:
                names = line.rstrip()
                l = 2
            elif l == 2:
                pas = line.rstrip('\n')
                l = 3
            else:
                y = {names: [pas, float(line.rstrip('\n'))]}
                self.lasts.update(y)
                l = 1
            r = r + 1
        self.f.close()
        if r < 3 or r % 3 != 0:
            self.f = open('lastpas.txt', 'w')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write('Admin')
            self.f.write('\n')
            self.f.write(str(time.time()))
            self.f.write('\n')
            self.f.close()
        print(self.lasts.items())

    def backtouserspacedialog(self):
        if self.name != 'Admin':
            self.openuserspacedialog()
        # else:
        #     self.wind = Ui_Adminmenu_2()
        #     self.wind.show()
        #     self.wind.backbutton()
        #     self.close()

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
        self.readparam()
        self.readusers()
        self.readlastpass()
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
        if self.spec:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name]) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name]) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name]) or \
                    set("1234567890").isdisjoint(self.users[self.name]):
                self.message('You must use special symbols, numbers and letters of different registers in your pass!')
                self.opennewpassformdialogad()
        if len(self.users[self.name]) < self.mindlin:
            self.message('Your pass is so short, min length is ' + str(self.mindlin))
            self.opennewpassformdialogad()

    def opennewpassformdialogad(self):
        self.dialog = Ui_Newpassform()
        self.dialog.setupUi(self)
        self.dialog.Back.clicked.connect(self.backbutton)
        self.dialog.Newpasssubmit.clicked.connect(self.createnewpassad)

    def createnewpassad(self):
        self.newpass = self.dialog.Newuserpass.text()
        if time.time()-self.lasts[self.name][1]<self.mintime:
            self.message('You mast wait ' + str(self.mintime-int(time.time()-self.lasts[self.name][1])) + ' seconds')
            self.backbutton()
        elif len(self.dialog.Newuserpass.text()) < self.mindlin:
            self.message('Pass is so short, min length is ' + str(self.mindlin))
        elif self.spec:
            if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
                    set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
                    set("1234567890").isdisjoint(self.newpass):
                self.message('You must use special symbols, numbers and letters of different registers')
            else:
                self.users[self.name] = self.newpass
                self.user = ''
                self.writeusers()
                self.lasts[self.name][0] = self.newpass
                self.lasts[self.name][1] = time.time()
                self.writelastpass()
                self.message('Successful new pass')
                self.backbutton()
        else:
            self.users[self.name] = self.newpass
            self.user = ''
            self.writeusers()
            self.lasts[self.name][0] = self.newpass
            self.lasts[self.name][1] = time.time()
            self.writelastpass()
            self.message('Successful new pass')
            self.backbutton()

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
            self.f = open('user.txt', 'a')
            self.f.write(self.dialognu.Newusername.text())
            self.f.write('\n*')
            self.f.write('\n')
            self.f.close()
            self.f = open('lastpas.txt', 'a')
            self.f.write(self.dialognu.Newusername.text())
            self.f.write('\n*')
            self.f.write('\n')
            self.f.write('0')
            self.f.write('\n')
            self.f.close()
            self.message('User \"' + self.dialognu.Newusername.text() + '\" is created')
            self.backbutton()

    def openlistofusersdialog(self):
        self.readusers()
        self.dialog = Ui_Listofusers()
        self.dialog.setupUi(self)
        for self.user in self.users:
            self.dialog.Userslist.addItems([self.user])
        self.dialog.deleteuserButton.clicked.connect(self.deletinguser)
        self.dialog.Back.clicked.connect(self.backbutton)

    def deletinguser(self):
        self.user = self.dialog.Userslist.currentText()
        if self.user == 'Admin':
            self.message('Admin can\'t be deleted!')
        else:
            self.writeusers()
            self.writelastpass()
            self.message('User \"' + self.user + '\" deleted')
            self.openlistofusersdialog()

    def openchooseoptionsformdialog(self):
        self.dialogop = Ui_Chooseoptionsform()
        self.dialogop.setupUi(self)
        self.dialogop.Mindlin.setValue(self.mindlin)
        self.dialogop.Mintime.setValue(self.mintime)
        self.dialogop.checsimvol.setChecked(self.spec)
        self.dialogop.Submit.clicked.connect(self.submitoptions)

    def submitoptions(self):
        self.mindlin = self.dialogop.Mindlin.value()
        self.mintime = self.dialogop.Mintime.value()
        self.spec = self.dialogop.checsimvol.isChecked()
        self.writeparam()
        self.backbutton()

    def writeparam(self):
        self.f = open('param.txt', 'w')
        self.f.write(str(self.mindlin))
        self.f.write('\n')
        self.f.write(str(self.mintime))
        self.f.write('\n')
        if self.spec:
            self.f.write('1')
        else:
            self.f.write('0')
        self.f.close()

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
