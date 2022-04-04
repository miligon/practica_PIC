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
        MainWindow.resize(577, 645)
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
        self.groupBox_2.setGeometry(QtCore.QRect(380, 10, 191, 61))
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnAdquirir = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAdquirir.setGeometry(QtCore.QRect(10, 30, 80, 23))
        self.btnAdquirir.setObjectName("btnAdquirir")
        self.btnMotor = QtWidgets.QPushButton(self.groupBox_2)
        self.btnMotor.setGeometry(QtCore.QRect(100, 30, 80, 23))
        self.btnMotor.setObjectName("btnMotor")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 80, 561, 431))
        self.widget.setObjectName("widget")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 520, 561, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.radioSobre = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioSobre.setGeometry(QtCore.QRect(10, 30, 141, 21))
        self.radioSobre.setChecked(True)
        self.radioSobre.setObjectName("radioSobre")
        self.radioSub = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioSub.setGeometry(QtCore.QRect(160, 30, 131, 21))
        self.radioSub.setObjectName("radioSub")
        self.txtWn = QtWidgets.QLineEdit(self.groupBox_3)
        self.txtWn.setGeometry(QtCore.QRect(300, 30, 113, 23))
        self.txtWn.setObjectName("txtWn")
        self.txtZ = QtWidgets.QLineEdit(self.groupBox_3)
        self.txtZ.setGeometry(QtCore.QRect(430, 30, 113, 23))
        self.txtZ.setObjectName("txtZ")
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
        self.groupBox_3.setTitle(_translate("MainWindow", "Seleccion tipo de sistema"))
        self.radioSobre.setText(_translate("MainWindow", "Sobreamortiguado"))
        self.radioSub.setText(_translate("MainWindow", "Subamortiguado"))

