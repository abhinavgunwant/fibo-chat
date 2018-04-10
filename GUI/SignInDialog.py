import re
import sys
import PyQt5
import DBInit
import GUI.MainWindowGUI
import GUI.SignInDialogGUI
from chatGUI import server,client
from chatGUI.server import Window


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog
from GUI.SignInDialogGUI import Ui_Dialog
from PyQt5              import QtCore, QtGui, QtWidgets
from PyQt5.QtCore       import QCoreApplication

app             = QApplication(sys.argv)
window    = Window()


class SignInDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.signinButton.clicked.connect(self.signIn)
    
    def signIn(self):
        username = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()
                
        result = DBInit.loginCheck(username,password)
        if(result):
            self.showMessage("Logged in Successfully","Logged In Successfully")
            print(result)
            self.formReset()
            window.show()
            
            
            
            
        else:
            print("password wrong")
            self.showMessage("Warning","Invalid Username and Password")
            self.formReset()
            
    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()


    def formReset(self):
        print('reset form....')
        self.ui.usernameEdit.setText('')
        self.ui.passwordEdit.setText('')