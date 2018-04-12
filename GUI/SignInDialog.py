import re
import sys
import PyQt5
import DBInit
import GUI.MainWindowGUI
import GUI.SignInDialogGUI
import json
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

        self.sock = None
        self.signedIn = False
        self.username = ''

    def getSignedIn(self):
        return self.signedIn

    def getUsername(self):
        return self.username

    def setSock(self, sock):
        self.sock = sock
    
    def signIn(self):
        username = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()

        # result = DBInit.loginCheck(username,password)

        reqObj = {
            'type':     'login',
            'username': username,
            'password': password
        }

        reqJson = json.dumps(reqObj)

        self.sock.send(bytes(reqJson, 'utf-8'))
        respJson = self.sock.recv(1024).strip().decode()
        respObj = json.loads(respJson)

        if 'type' in respObj:
            if respObj['type']:
                # self.showMessage("Logged in Successfully","Logged In Successfully")
                # print(result)
                self.formReset()
                # window.show()
                self.signedIn = True
                self.hide()
            else:
                print("password wrong")
                self.showMessage("Warning","Invalid Username and Password")
                self.formReset()
        else:
            self.showMessage('Error!', 'There was error communicating server, please try after some time...')
            
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

    # def displayLoginDialog(self):
    #     print('show sign-in dialog')

        # self.show()

        # while not self.signedIn:
        #     if self.signedIn:
        #         break

        # return self.username