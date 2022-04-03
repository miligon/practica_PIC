# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(577, 546)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 351, 61))
        self.groupBox.setObjectName("groupBox")
        self.txtPuerto = QtWidgets.QLineEdit(self.groupBox)
        self.txtPuerto.setGeometry(QtCore.QRect(10, 30, 241, 23))
        self.txtPuerto.setObjectName("txtPuerto")
        self.btnConectar = QtWidgets.QPushButton(self.groupBox)
        self.btnConectar.setGeometry(QtCore.QRect(260, 30, 80, 23))
        self.btnConectar.setObjectName("btnConectar")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(370, 10, 191, 61))
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnAdquirir = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAdquirir.setGeometry(QtCore.QRect(10, 30, 80, 23))
        self.btnAdquirir.setObjectName("btnAdquirir")
        self.btnMotor = QtWidgets.QPushButton(self.groupBox_2)
        self.btnMotor.setGeometry(QtCore.QRect(100, 30, 80, 23))
        self.btnMotor.setObjectName("btnMotor")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 80, 551, 431))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Adquision de datos"))
        self.groupBox.setTitle(_translate("MainWindow", "Conexión"))
        self.txtPuerto.setText(_translate("MainWindow", "/dev/ttyACM0"))
        self.btnConectar.setText(_translate("MainWindow", "Conectar"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Acciones"))
        self.btnAdquirir.setText(_translate("MainWindow", "Adquirir"))
        self.btnMotor.setText(_translate("MainWindow", "Motor: OFF"))

