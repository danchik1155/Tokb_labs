# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/Chooseoptionsform2.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Chooseoptionsform(object):
    def setupUi(self, Chooseoptionsform):
        Chooseoptionsform.setObjectName("Chooseoptionsform")
        Chooseoptionsform.resize(285, 153)
        self.centralwidget = QtWidgets.QWidget(Chooseoptionsform)
        self.centralwidget.setObjectName("centralwidget")
        self.Mintime = QtWidgets.QSpinBox(self.centralwidget)
        self.Mintime.setGeometry(QtCore.QRect(210, 37, 42, 22))
        self.Mintime.setMinimum(1)
        self.Mintime.setObjectName("Mintime")
        self.checsimvol = QtWidgets.QCheckBox(self.centralwidget)
        self.checsimvol.setGeometry(QtCore.QRect(10, 67, 261, 31))
        self.checsimvol.setObjectName("checsimvol")
        self.Submit = QtWidgets.QPushButton(self.centralwidget)
        self.Submit.setGeometry(QtCore.QRect(110, 107, 75, 23))
        self.Submit.setObjectName("Submit")
        self.Mindlin = QtWidgets.QSpinBox(self.centralwidget)
        self.Mindlin.setGeometry(QtCore.QRect(210, 7, 42, 22))
        self.Mindlin.setMinimum(1)
        self.Mindlin.setObjectName("Mindlin")
        self.Mindlintext = QtWidgets.QLabel(self.centralwidget)
        self.Mindlintext.setGeometry(QtCore.QRect(20, 10, 151, 16))
        self.Mindlintext.setObjectName("Mindlintext")
        self.Mintimetext = QtWidgets.QLabel(self.centralwidget)
        self.Mintimetext.setGeometry(QtCore.QRect(20, 40, 191, 31))
        self.Mintimetext.setObjectName("Mintimetext")
        self.Deactivate = QtWidgets.QPushButton(self.centralwidget)
        self.Deactivate.setGeometry(QtCore.QRect(200, 107, 75, 23))
        self.Deactivate.setObjectName("Deactivate")
        self.Activate = QtWidgets.QPushButton(self.centralwidget)
        self.Activate.setGeometry(QtCore.QRect(20, 107, 75, 23))
        self.Activate.setObjectName("Activate")
        Chooseoptionsform.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Chooseoptionsform)
        self.statusbar.setObjectName("statusbar")
        Chooseoptionsform.setStatusBar(self.statusbar)

        self.retranslateUi(Chooseoptionsform)
        QtCore.QMetaObject.connectSlotsByName(Chooseoptionsform)

    def retranslateUi(self, Chooseoptionsform):
        _translate = QtCore.QCoreApplication.translate
        Chooseoptionsform.setWindowTitle(_translate("Chooseoptionsform", "Choose options form"))
        self.checsimvol.setText(_translate("Chooseoptionsform", "обязательное использование спец. символов\n"
" (!@&*#?), цифр, букв разных регистров"))
        self.Submit.setText(_translate("Chooseoptionsform", "Submit"))
        self.Mindlintext.setText(_translate("Chooseoptionsform", "Минимальная длина пароля"))
        self.Mintimetext.setText(_translate("Chooseoptionsform", "Минимальная срок действия пароля\n"
"      (сек)"))
        self.Deactivate.setText(_translate("Chooseoptionsform", "Deactivate"))
        self.Activate.setText(_translate("Chooseoptionsform", "Activate"))
