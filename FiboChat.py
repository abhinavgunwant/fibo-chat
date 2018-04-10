import sys
import sqlite3
import DBInit
import PyQt5
import _thread

from PyQt5              import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets    import QWidget, QApplication
from PyQt5.QtCore       import QCoreApplication
from GUI.MainWindow     import MainWindow
from GUI.SignInDialog   import SignInDialog
from GUI.RegisterDialog import RegisterDialog

from socket             import *

username = ''
signedIn = False

def launchRegisterDiag():
    global regDialog
    global sock

    signInDialog.hide()
    regDialog.setSock(sock)

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

def checkSignedIn():
    global signInDialog
    global username

    print('checkSignedIn(): start')
    while True:
        if signInDialog.getSignedIn():
            break

    username = signInDialog.getUsername()
    signedIn = True
    signInDialog.hide()
    print('checkSignedIn(): end with login!')
    
    return True
        

dbConn = sqlite3.connect('data.db')
dbCur = dbConn.cursor()

DBInit.init()

host = "127.168.2.75"
port=4447

sock=socket(AF_INET, SOCK_STREAM)
sock.connect((host,port))

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

signInDialog.setSock(sock)

if len(list(x)) == 0:
    # open the login dialog
    mainWindow.ui.friendsOnlineLabel.setText('You Must Login to continue...')
    mainWindow.ui.label.setText('<font color="RED"><b>You are not Logged In!</b></font>')
    mainWindow.ui.friendListView.hide()

    username = signInDialog.show()
else:
    username = signInDialog.show()

# signInDialog.hide()

_thread.start_new_thread(checkSignedIn, ())



sys.exit(app.exec_())