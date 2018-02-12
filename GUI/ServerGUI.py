# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ServerGUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.logBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logBrowser.setGeometry(QtCore.QRect(5, 41, 791, 501))
        self.logBrowser.setObjectName("logBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label.setObjectName("label")
        self.serverStatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.serverStatusLabel.setGeometry(QtCore.QRect(120, 10, 55, 16))
        self.serverStatusLabel.setObjectName("serverStatusLabel")
        self.serverStartStopButton = QtWidgets.QPushButton(self.centralwidget)
        self.serverStartStopButton.setGeometry(QtCore.QRect(180, 0, 93, 41))
        self.serverStartStopButton.setObjectName("serverStartStopButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Server = QtWidgets.QAction(MainWindow)
        self.actionNew_Server.setObjectName("actionNew_Server")
        self.actionLoad_Custom_Settings = QtWidgets.QAction(MainWindow)
        self.actionLoad_Custom_Settings.setObjectName("actionLoad_Custom_Settings")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionEcit = QtWidgets.QAction(MainWindow)
        self.actionEcit.setObjectName("actionEcit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionNew_Server)
        self.menuFile.addAction(self.actionLoad_Custom_Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionEcit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fibochat Server"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Server Status:</span></p></body></html>"))
        self.serverStatusLabel.setText(_translate("MainWindow", "Offline"))
        self.serverStartStopButton.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Server.setText(_translate("MainWindow", "New Server"))
        self.actionLoad_Custom_Settings.setText(_translate("MainWindow", "Load Custom Settings"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionEcit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

