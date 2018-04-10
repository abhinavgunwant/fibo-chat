import re
import DBInit
import sys
import PyQt5
import json
import GUI.MainWindowGUI
import GUI.RegisterDialogGUI
import GUI.SignInDialogGUI
import FiboCrypt.fibocrypt as fc

from PyQt5                      import QtGui, QtWidgets
from PyQt5.QtWidgets            import QWidget, QApplication, QMainWindow, QDialog

from GUI.RegisterDialogGUI      import Ui_Register
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtCore               import QCoreApplication
from GUI.MainWindow             import MainWindow
from GUI.SignInDialog           import SignInDialog
# from FiboCrypt.fibocrypt        import fibocrypt, toString

app             = QApplication(sys.argv)
signInDialog    = SignInDialog()

class RegisterDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Register()
        self.ui.setupUi(self)

        self.ui.registerButton.clicked.connect(self.register)
        self.ui.resetButton.clicked.connect(self.formReset)

        self.emailPattern = r'^(\w|[\._\-0-9])+@(\w|[\-0-9])+(\.\w+)+$'

        # socket object
        self.sock = None

    def setSock(self, sock):
        self.sock = sock

    def register(self):
        print('register....')
        formValid = True
        registerNotificationText = 'Registration in progress... Please wait...'
        # self.ui.registerNotificationLabel.setText()
        username = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()
        confPass = self.ui.confPassEdit.text()
        email = self.ui.emailEdit.text()
        firstName = self.ui.firstNameEdit.text()
        lastName = self.ui.lastNameEdit.text()

        if password != confPass:
            print('ERROR: Passwords do not match!')
            # self.ui.registerNotificationLabel.setText(
            registerNotificationText += '<br /><font color="red">Error: The passwords do not match!</font>'
            # )
            # return
            formValid = False
        
        if self.checkFields(firstName,username,email,password):
            # self.ui.registerNotificationLabel.setText(
            registerNotificationText += '<br /><font color="red">Error: All fields must be filled</font>'
            # )
            # return
            formValid = False
            
        if not bool(re.match(self.emailPattern, email)):
            # self.ui.registerNotificationLabel.setText(
            registerNotificationText += '<br /><font color="red">Error: The email is not valid!</font>'
            # )
            # return
            formValid = False           

        #passwordSecure = fc.toString(fc.fibocrypt(password, 1, 2))
        self.ui.registerNotificationLabel.setText(registerNotificationText)

        if not formValid:
            return
        
        
        else:
            if password == confPass:
                # DBInit.insertTable(firstName,lastName,username,email,password)

                regObj = {
                    'type': 'register',
                    'firstName': firstName,
                    'lastName': lastName,
                    'username': username,
                    'email': email,
                    'password': password
                }
                
                # regObj = {
                #     'type': 'register',
                #     'firstName': 'firstName',
                #     'lastName': 'lastName',
                #     'username': 'username',
                #     'email': 'email@gmail.com',
                #     'password': 'password'
                # }

                self.sock.send(bytes(json.dumps(regObj), 'utf-8'))
                regSuccessful = False

                # while not regSuccessful:
                respData = self.sock.recv(1024).strip().decode()
                respObj = json.loads(respData)

                if 'type' in respObj and respObj['type'] == 'status':
                    if respObj['status']:                
                        self.showMessage("Success","Registration successul")
                        self.formReset()
                    else:
                        self.showMessage('Error!', respObj['message'])
                else:
                    self.showMessage('Error!', respObj['message'])
        
    def checkFields(self,firstName,username,email,password):
        if(username=="" or firstName=="" or email == "" or password== ""):
            return True    
    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
        signInDialog.show()
        RegisterDialog.hide(self)

        ## send the regObj to the server

    def formReset(self):
        print('reset form....')
        self.ui.firstNameEdit.setText('')
        self.ui.lastNameEdit.setText('')
        self.ui.emailEdit.setText('')
        self.ui.usernameEdit.setText('')
        self.ui.passwordEdit.setText('')
        self.ui.confPassEdit.setText('')
