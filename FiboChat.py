import sys
import sqlite3
import DBInit
import PyQt5
import _thread
import json
import FiboCrypt.fibocrypt as fc
import FiboCrypt.Util

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
from FiboCrypt.Util     import randomInt

from socket             import *

exit                = False
username            = ''
signedIn            = False
contactsList        = []
contactsOnline      = []
openedChatDialogs   = []
dbConn              = None
dbCur               = None
sock                = None
signInDialog        = None
mainWindow          = None
regDialog           = None

logfile             = open('client-log.txt', 'w')

## Default host and port:
# host                = "192.168.43.12"
# host                = "192.168.43.64"
# host                = "10.20.4.203"
host                = "10.20.4.108"
# host                = "localhost"
port                = 4447

preSharedKeys       = {
    'p': 0,
    'q': 0
}

def launchRegisterDiag():
    global regDialog
    global sock
    global signInDialog

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

    firstName   = regDialog.ui.firstNameEdit.text()
    lastName    = regDialog.ui.lastNameEdit.text()
    email       = regDialog.ui.emailEdit.text()
    username    = regDialog.ui.usernameEdit.text()
    password    = regDialog.ui.passwordEdit.text()

    print('Register\nFirst Name: '+firstName+'\nLast Name: '+lastName)
    print('Email: '+email+'\nUsername: '+username+'\nPassword: '+password)

def checkSignedIn():
    global signInDialog
    global username
    global signedIn
    global sock
    global logfile

    print('checkSignedIn(): start')
    while True:
        if signInDialog.getSignedIn():
            break

    username = signInDialog.getUsername()
    signedIn = True
    signInDialog.hide()
    print('checkSignedIn(): logged in as: ' + username)
    logfile.write('\ncheckSignedIn(): logged in as: ' + username)

    print('checkSignedIn(): now getting contacts...')
    
    ## now get the online contacts
    sock.send(bytes(json.dumps({'type': 'contactlist'}), 'utf-8'))
    # respData        = sock.recv(1024).strip().decode()
    respData        = sock.recv(1024).strip().decode()
    respObj         = json.loads(respData)
    print(respObj)
    contactsList    = respObj['contacts']
    contactsOnline  = respObj['contactsonline']

    # loadContactList(contactList)
    contactListModel = QStandardItemModel(mainWindow.ui.friendListView)
    for contact in contactsList:
        listEntryText =  contact[0] + ' ' + contact[1] + ' (' + contact[2] + ')'
        cItem = QStandardItem(listEntryText)
        cItem.setFont(QFont("Helvetica [Cronyx]", 14))
        if contact[2] in contactsOnline:
            ## show online contacts as green
            cItem.setForeground(Qt.green)
        else:
            ## show offline contacts as black
            cItem.setForeground(Qt.black)
            
        contactListModel.appendRow(cItem)

    mainWindow.ui.friendListView.setModel(contactListModel)
    mainWindow.ui.friendListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    mainWindow.ui.friendListView.show()

    return True

def loadContactList(contactList):
    global mainWindow
    ## add contacts to list view
    contactListModel = QStandardItemModel(mainWindow.ui.friendListView)
    for contact in contactsList:
        listEntryText =  contact[0] + ' ' + contact[1] + ' (' + contact[2] + ')'
        cItem = QStandardItem(listEntryText)
        cItem.setFont(QFont("Helvetica [Cronyx]", 14))
        if contact[2] in contactsOnline:
            ## show online contacts as green
            cItem.setForeground(Qt.green)
        else:
            ## show offline contacts as black
            cItem.setForeground(Qt.black)
            
        contactListModel.appendRow(cItem)

    mainWindow.ui.friendListView.setModel(contactListModel)
    mainWindow.ui.friendListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    mainWindow.ui.friendListView.show()


def onContactSelect(index):
    print(index.data())

def newChatDialog(index):
    global username
    global sock

    ## index.data() contains the text of the QListView object which is
    ##      of the format: "FirstName LastName (username)"
    ##      we are interested in extracting username from this string...
    rightOfParenthesis = index.data().split('(')[1]
    contact = rightOfParenthesis.split(')')[0]

    chatDialog = ChatDialog()

    openedChatDialogs.append({'contact': contact, 'chatDialogObject': chatDialog, 'preSharedKeys':{'p': 0, 'q': 0}})

    chatDialog.setUser(username)
    chatDialog.setContact(contact)
    chatDialog.setSock(sock)
    chatDialog.ui.setWindowTitle('Chat: ' + contact)
    _thread.start_new_thread(messageListener, (chatDialog, contact,))

    chatDialog.ui.exec()

def messageListener(chatDialog, contact):
    global sock
    global logfile
    print('listening messages at....'+str(sock.getpeername())+', '+str(sock.getsockname()))
    logfile.write('\nlistening messages at....'+str(sock.getpeername())+', '+str(sock.getsockname()))
    print('Sharing keys for this client...')
    keyP = randomInt(5)
    keyQ = randomInt(5)
    chatDialog.setPreSharedKeys(keyP, keyQ)

    ## share the 'preshared key' with the other connected client
    sock.send(bytes(json.dumps({
        'type': 'keyshare',
        'touser': contact,
        'fromuser': username,
        'keys':{
            'p': keyP,
            'q': keyQ
        }}), 'utf-8'))
    
    chatDialog = None
    chatDiagObj = None

    for dlog in openedChatDialogs:
        if dlog['contact'] == contact:
            hasOpenedChatDialog = True
            chatDialog = dlog['chatDialogObject']
            chatDiagObj = dlog
            break

    print('setting preSharedKeys...\nP: ' + str(keyP) + ' Q: ' + str(keyQ))
    logfile.write('\nsetting preSharedKeys...\nP: ' + str(keyP) + ' Q: ' + str(keyQ))
    chatDiagObj['preSharedKeys']['p'] = keyP
    chatDiagObj['preSharedKeys']['q'] = keyQ

    hasOpenedChatDialog = False
    messageText = ''
    
    while not exit:
        data = sock.recv(65535).strip().decode()
        print('received: ' + data)
        logfile.write('\nreceived: ' + data)
        dataJson = json.loads(data)

        if 'type' in dataJson and dataJson['type'] == 'keyshare' and dataJson['touser'] == username:
            print('Received keyshare request from: '+dataJson['fromuser'])
            logfile.write('\nReceived keyshare request from: '+dataJson['fromuser'])
            for i in range(len(openedChatDialogs)):
                if openedChatDialogs[i]['contact'] == dataJson['fromuser']:
                    print('setting preSharedKeys...\nP: ' + str(dataJson['keys']['p']) + ' Q: ' + str(dataJson['keys']['q']))
                    logfile.write('\nsetting preSharedKeys...\nP: ' + str(dataJson['keys']['p']) + ' Q: ' + str(dataJson['keys']['q']))
                    openedChatDialogs[i]['preSharedKeys']['p'] = dataJson['keys']['p']
                    openedChatDialogs[i]['preSharedKeys']['q'] = dataJson['keys']['q']
                    chatDialog.setPreSharedKeys(dataJson['keys']['p'], dataJson['keys']['q'])
                    break
            
        elif 'type' in dataJson and dataJson['type'] == 'message' and dataJson['touser'] == username:
            messageText = fc.decryptFromString(dataJson['message'], chatDiagObj['preSharedKeys'])
            print('verifying this message...')
            logfile.write('\nverifying this message...')
            cryptList, p_, q_ = fc.fromString(dataJson['message'], chatDiagObj['preSharedKeys'])
            print(cryptList[0].tolist())
            if fc.verifyAll(cryptList):
                print('message verification succeeded!')
                logfile.write('\nmessage verification succeeded!')
            else:
                print('message may be corrupt!')
                logfile.write('\nmessage may be corrupt!')
            DBInit.insertMessage(username, dataJson['fromuser'], 'I', messageText)

            print('showing in chat dialog...')
            logfile.write('\nshowing in chat dialog...')
            chatDialog.receive(dataJson['fromuser'], messageText)
            DBInit.insertMessage(username, dataJson['fromuser'], 'I', messageText)
        elif 'type' in dataJson and dataJson['type'] == 'contactlist':
            # contactsRecvData = json.loads(dataJson)
            loadContactList(dataJson['contacts'])


def loadClientConfig():
    global host
    global port

    configStr = ''

    with open('config.json') as configFile:
        for line in configFile:
            configStr += line

    configJson  = json.loads(configStr)
    host        = configJson['host']
    port        = int(configJson['port'])


def main():
    global dbConn
    global dbCur
    global sock
    global signInDialog
    global mainWindow
    global regDialog

    dbConn  = sqlite3.connect('data.db')
    dbCur   = dbConn.cursor()

    ## load the hostname and port info from config.json
    # loadClientConfig()

    DBInit.init()

    sock            = socket(AF_INET, SOCK_STREAM)
    sock.connect((host,port))

    app             = QApplication(sys.argv)
    mainWindow      = MainWindow()
    regDialog       = RegisterDialog()
    signInDialog    = SignInDialog()


    signInDialog.ui.registerButton.clicked.connect(launchRegisterDiag)
    regDialog.ui.resetButton.clicked.connect(resetRegisterDiag)
    regDialog.ui.registerButton.clicked.connect(register)
    mainWindow.ui.friendListView.doubleClicked.connect(newChatDialog)

    ## Check if the user token is stored...
    x = dbCur.execute('SELECT * FROM USER')

    mainWindow.show()

    signInDialog.setSock(sock)

    if len(list(x)) == 0:
        ## open the login dialog
        mainWindow.ui.friendsOnlineLabel.setText('You Must Login to continue...')
        mainWindow.ui.label.setText('<font color="RED"><b>You are not Logged In!</b></font>')
        mainWindow.ui.friendListView.hide()

        signInDialog.show()
    else:
        signInDialog.show()

    _thread.start_new_thread(checkSignedIn, ())

    sys.exit(app.exec_())


## Make sure it is not started as a module...
if __name__ == '__main__':
    main()
else:
    print('This module should be started as a standalone python program...')