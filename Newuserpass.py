# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/Newuserpass2.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Newpassform(object):
    def setupUi(self, Newpassform):
        Newpassform.setObjectName("Newpassform")
        Newpassform.resize(285, 150)
        self.centralwidget = QtWidgets.QWidget(Newpassform)
        self.centralwidget.setObjectName("centralwidget")
        self.Olduserpass = QtWidgets.QLineEdit(self.centralwidget)
        self.Olduserpass.setGeometry(QtCore.QRect(10, 10, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Olduserpass.setFont(font)
        self.Olduserpass.setObjectName("Olduserpass")
        self.Newpasssubmit = QtWidgets.QPushButton(self.centralwidget)
        self.Newpasssubmit.setGeometry(QtCore.QRect(20, 100, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Newpasssubmit.setFont(font)
        self.Newpasssubmit.setObjectName("Newpasssubmit")
        self.Back = QtWidgets.QPushButton(self.centralwidget)
        self.Back.setGeometry(QtCore.QRect(150, 100, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Back.setFont(font)
        self.Back.setObjectName("Back")
        self.Newuserpass = QtWidgets.QLineEdit(self.centralwidget)
        self.Newuserpass.setGeometry(QtCore.QRect(10, 60, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Newuserpass.setFont(font)
        self.Newuserpass.setObjectName("Newuserpass")
        Newpassform.setCentralWidget(self.centralwidget)

        self.retranslateUi(Newpassform)
        QtCore.QMetaObject.connectSlotsByName(Newpassform)

    def retranslateUi(self, Newpassform):
        _translate = QtCore.QCoreApplication.translate
        Newpassform.setWindowTitle(_translate("Newpassform", "Change pass form"))
        self.Olduserpass.setPlaceholderText(_translate("Newpassform", "Old user pass..."))
        self.Newpasssubmit.setText(_translate("Newpassform", "Submit"))
        self.Back.setText(_translate("Newpassform", "Back"))
        self.Newuserpass.setPlaceholderText(_translate("Newpassform", "New user pass..."))
