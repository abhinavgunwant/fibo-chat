import sys
import sqlite3
import DBInit
import PyQt5
import _thread
import json
import FiboCrypt.fibocrypt as fc

import numpy as np

from PyQt5              import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets    import QWidget, QApplication, QAbstractItemView
from PyQt5.QtCore       import QCoreApplication, Qt
from PyQt5.QtGui        import QStandardItemModel, QStandardItem, QFont
from GUI.MainWindow     import MainWindow
from GUI.SignInDialog   import SignInDialog
from GUI.RegisterDialog import RegisterDialog
from GUI.ChatDialog     import ChatDialog
from GUI.ChatDialogGUI  import Ui_Chat

from socket             import *


p = 43566776258855008468992
q = 70492524767089384226816

exit = False
username = ''
signedIn = False
contactsList = []
contactsOnline = []
openedChatDialogs = []

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
    global signedIn
    global sock

    print('checkSignedIn(): start')
    while True:
        if signInDialog.getSignedIn():
            break

    username = signInDialog.getUsername()
    signedIn = True
    signInDialog.hide()
    print('checkSignedIn(): logged in as: ' + username)

    print('checkSignedIn(): now getting contacts...')
    
    # now get the online contacts
    sock.send(bytes(json.dumps({'type': 'contactlist'}), 'utf-8'))
    respData = sock.recv(1024).strip().decode()
    respObj = json.loads(respData)
    print(respObj)
    contactsList = respObj['contacts']
    contactsOnline = respObj['contactsonline']

    # add contacts to list view
    contactListModel = QStandardItemModel(mainWindow.ui.friendListView)
    for contact in contactsList:
        listEntryText =  contact[0] + ' ' + contact[1] + ' (' + contact[2] + ')'
        cItem = QStandardItem(listEntryText)
        cItem.setFont(QFont("Helvetica [Cronyx]", 14))
        if contact[2] in contactsOnline:
            # listEntryText = '<font color="green">'+contact[0] + ' ' + contact[1]+'</font>'
            cItem.setForeground(Qt.green)
        else:
            # listEntryText = '<font color="black">'+contact[0] + ' ' + contact[1]+'</font>'
            cItem.setForeground(Qt.black)
            
        contactListModel.appendRow(cItem)

    mainWindow.ui.friendListView.setModel(contactListModel)
    mainWindow.ui.friendListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    mainWindow.ui.friendListView.show()

    # _thread.start_new_thread(messageListener, ())        
    return True 
        

def onContactSelect(index):
    # mainWindow.ui.friendListView.
    print(index.data())


def newChatDialog(index):
    global username
    global sock
    print('!!', index.data())

    _thread.start_new_thread(messageListener, ())

    # index.data() contains the text of the QListView item which is 
    # like: "FirstName LastName (username)"
    # we are interested in extracting username from this string...
    rightOfParenthesis = index.data().split('(')[1]
    contact = rightOfParenthesis.split(')')[0]

    chatDialog = ChatDialog()

    openedChatDialogs.append({'contact': contact, 'chatDialogObject': chatDialog})

    chatDialog.setUser(username)
    chatDialog.setContact(contact)
    chatDialog.setSock(sock)
    chatDialog.ui.setWindowTitle('Chat: ' + contact)

    chatDialog.ui.exec()
    # messageListener()

def messageListener():
    global sock
    print('listening messages at....'+str(sock.getpeername())+', '+str(sock.getsockname()))
    # global DBInit
    hasOpenedChatDialog = False
    chatDialog = None
    messageText = ''
    while not exit:
        print('before receiving...')
        data = sock.recv(65535).strip().decode()
        print('received: ' + data)
        dataJson = json.loads(data)
        if 'type' in dataJson and dataJson['type'] == 'message' and dataJson['touser'] == username:
            # cl = list(dataJson['message'])
            # cryptList = []
            # for i in cl:
            #     j = np.matrix(i)
            #     cryptList.append(j)

            messageText = fc.decryptFromString(dataJson['message'])

            # DBInit.insertMessage(username, dataJson['fromuser'], 'I', dataJson['message'])
            DBInit.insertMessage(username, dataJson['fromuser'], 'I', messageText)

            for dlog in openedChatDialogs:
                if dlog['contact'] == dataJson['fromuser']:
                    hasOpenedChatDialog = True
                    chatDialog = dlog['chatDialogObject']
                    break
            
            if hasOpenedChatDialog:
                # chatDialog.receive(dataJson['fromuser'], dataJson['message'])
                chatDialog.receive(dataJson['fromuser'], messageText)

            # DBInit.insertMessage(username, dataJson['fromuser'], 'I', dataJson['message'])
            DBInit.insertMessage(username, dataJson['fromuser'], 'I', messageText)

dbConn = sqlite3.connect('data.db')
dbCur = dbConn.cursor()

DBInit.init()

host = '127.0.0.1'
# host = "127.168.2.75"
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
mainWindow.ui.friendListView.doubleClicked.connect(newChatDialog)
# mainWindow.ui.friendListView.clicked.connect(onContactSelect)

# Check if the user token is stored...
x = dbCur.execute('SELECT * FROM USER')

mainWindow.show()

signInDialog.setSock(sock)

if len(list(x)) == 0:
    # open the login dialog
    mainWindow.ui.friendsOnlineLabel.setText('You Must Login to continue...')
    mainWindow.ui.label.setText('<font color="RED"><b>You are not Logged In!</b></font>')
    mainWindow.ui.friendListView.hide()

    # username = signInDialog.show()
    signInDialog.show()
else:
    # username = signInDialog.show()
    signInDialog.show()

# signInDialog.hide()

_thread.start_new_thread(checkSignedIn, ())

sys.exit(app.exec_())