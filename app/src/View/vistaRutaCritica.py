# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vistaRutaCritica.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(940, 851)
        MainWindow.setStyleSheet("background-color: rgb(26, 74, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 451, 71))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 18pt \"Cambria\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 20, 301, 71))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 18pt \"Cambria\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(260, 140, 401, 71))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 18pt \"Cambria\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 480, 231, 41))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 18pt \"Cambria\";")
        self.label_4.setObjectName("label_4")
        self.reinscripcionBotton = QtWidgets.QPushButton(self.centralwidget)
        self.reinscripcionBotton.setGeometry(QtCore.QRect(370, 630, 171, 41))
        self.reinscripcionBotton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 16pt \"Cambria\";")
        self.reinscripcionBotton.setObjectName("reinscripcionBotton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(110, 720, 661, 71))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: italic 18pt \"Cambria\";")
        self.label_5.setObjectName("label_5")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(350, 260, 221, 191))
        self.photo.setMinimumSize(QtCore.QSize(0, 191))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("../../../../critical_path_implementacion/Resources/logoUP.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.matricula = QtWidgets.QTextEdit(self.centralwidget)
        self.matricula.setGeometry(QtCore.QRect(350, 540, 211, 41))
        self.matricula.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Cambria\";")
        self.matricula.setObjectName("matricula")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 940, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Universidad Politecnica De Chiapas"))
        self.label_2.setText(_translate("MainWindow", "Ingenieria En Software"))
        self.label_3.setText(_translate("MainWindow", "Metodo de la ruta critica de la \n"
"Carrera Ingenieria En Software"))
        self.label_4.setText(_translate("MainWindow", "Ingrese Matricula"))
        self.reinscripcionBotton.setText(_translate("MainWindow", "Ruta Critica"))
        self.label_5.setText(_translate("MainWindow", "Desarrollado por alumnos de ingenieria en software"))