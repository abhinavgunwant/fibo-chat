import sys
import sqlite3

import DBInit

import PyQt5

from PyQt5              import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets    import QWidget, QApplication
from PyQt5.QtCore       import QCoreApplication
from GUI.MainWindow     import MainWindow
from GUI.SignInDialog   import SignInDialog
from GUI.RegisterDialog import RegisterDialog


def launchRegisterDiag():
    global regDialog

    signInDialog.hide()

    regDialog.show()
    print('Launch Register Dialog')

def resetRegisterDiag():
    global regDialog

    regDialog.ui.firstNameEdit.setText('')
    regDialog.ui.lastNameEdit.setText('')
    regDialog.ui.emailEdit.setText('')
    regDialog.ui.usernameEdit.setText('')
    regDialog.ui.passwordEdit.setText('')
    regDialog.ui.confPassEdit.setText('')

def register():
    global regDialog

    firstName = regDialog.ui.firstNameEdit.text()
    lastName = regDialog.ui.lastNameEdit.text()
    email = regDialog.ui.emailEdit.text()
    username = regDialog.ui.usernameEdit.text()
    password = regDialog.ui.passwordEdit.text()

    print('Register\nFirst Name: '+firstName+'\nLast Name: '+lastName)
    print('Email: '+email+'\nUsername: '+username+'\nPassword: '+password)


dbConn = sqlite3.connect('data.db')
dbCur = dbConn.cursor()

DBInit.init()

app             = QApplication(sys.argv)
mainWindow      = MainWindow()
regDialog       = RegisterDialog()
signInDialog    = SignInDialog()

signInDialog.ui.registerButton.clicked.connect(launchRegisterDiag)
regDialog.ui.resetButton.clicked.connect(resetRegisterDiag)
regDialog.ui.registerButton.clicked.connect(register)

# Check if the user token is stored...
x = dbCur.execute('SELECT * FROM USER')

mainWindow.show()

if len(list(x)) == 0:
    # open the login dialog
    mainWindow.ui.friendsOnlineLabel.setText('You Must Login to continue...')
    mainWindow.ui.label.setText('<font color="RED"><b>You are not Logged In!</b></font>')
    mainWindow.ui.friendListView.hide()

    signInDialog.show()

sys.exit(app.exec_())
