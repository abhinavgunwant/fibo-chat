# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ServerSettingsDialogGUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ServerSettingsDialog(object):
    def setupUi(self, ServerSettingsDialog):
        ServerSettingsDialog.setObjectName("ServerSettingsDialog")
        ServerSettingsDialog.resize(435, 168)
        self.buttonBox = QtWidgets.QDialogButtonBox(ServerSettingsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 120, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(ServerSettingsDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 411, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)

        self.retranslateUi(ServerSettingsDialog)
        self.buttonBox.accepted.connect(ServerSettingsDialog.accept)
        self.buttonBox.rejected.connect(ServerSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ServerSettingsDialog)

    def retranslateUi(self, ServerSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        ServerSettingsDialog.setWindowTitle(_translate("ServerSettingsDialog", "FiboChat Server Settings"))
        self.label.setText(_translate("ServerSettingsDialog", "Server Name: "))
        self.label_2.setText(_translate("ServerSettingsDialog", "IP Address"))
        self.label_3.setText(_translate("ServerSettingsDialog", "Port"))

