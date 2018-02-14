import re
import sys
import PyQt5
import GUI.MainWindowGUI
import FiboCrypt.fibocrypt as fc

from PyQt5                      import QtGui, QtWidgets
from PyQt5.QtWidgets            import QWidget, QApplication, QMainWindow, QDialog
from GUI.RegisterDialogGUI      import Ui_Register
# from FiboCrypt.fibocrypt        import fibocrypt, toString

class RegisterDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Register()
        self.ui.setupUi(self)

        self.registerButton.clicked.connect(self.register)
        self.resetButton.clicked.connect(self.formReset)

        self.emailPattern = r'^(\w|[\._\-0-9])+@(\w|[\-0-9])+(\.\w+)+$'

    def register(self):
        print('register....')
        self.registerNotificationLabel.setText(
            'Registration in progress... Please wait...'
        )
        username = self.usernameEdit.getText()
        password = self.passwordEdit.getText()
        confPass = self.confPassEdit.getText()
        email = self.emailEdit.getText()
        firstName = self.firstNameEdit.getText()
        lastName = self.lastNameEdit.getText()

        if password != confPass:
            print('ERROR: Passwords do not match!')
            self.registerNotificationLabel.setText(
                '<font color="red">Error: The passwords do not match!</font>'
            )
            return

        if not bool(re.match(self.emailPattern, email)):
            self.registerNotificationLabel.setText(
                '<font color="red">Error: The email is not valid!</font>'
            )
            return

        passwordSecure = fc.toString(fc.fibocrypt(password, 1, 2))

        regObj = {
            'request-type': 'REGISTER',
            'payload':{
                'username': username,
                'password': passwordSecure,
                'first-name': firstName,
                'last-name': lastName,
                'email': email
            }
        }

        ## send the regObj to the server

    def formReset(self):
        print('reset form....')
        self.firstNameEdit.setText('')
        self.lastNameEdit.setText('')
        self.emailEdit.setText('')
        self.usernameEdit.setText('')
        self.passwordEdit.setText('')
        self.confPassEdit.setText('')
