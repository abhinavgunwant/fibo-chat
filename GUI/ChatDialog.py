import re
import DBInit
import sys
import PyQt5
import json
import GUI.MainWindowGUI
import GUI.RegisterDialogGUI
import GUI.SignInDialogGUI
import FiboCrypt.fibocrypt as fc
import FiboCrypt.Util

from PyQt5                      import QtGui, QtWidgets
from PyQt5.QtWidgets            import QWidget, QApplication, QMainWindow, QDialog

# from GUI.RegisterDialogGUI      import Ui_Register
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtCore               import QCoreApplication
from GUI.MainWindow             import MainWindow
from GUI.ChatDialogGUI          import Ui_Chat
from FiboCrypt.fibocrypt        import fibocrypt, toString
from FiboCrypt.Util             import fibNo, randomInt

# app             = QApplication(sys.argv)
# signInDialog    = SignInDialog()

# p = 43566776258855008468992
# q = 70492524767089384226816

p   = 1
q   = 2

class ChatDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Chat()

        self.user = None
        self.contact = None
        self.sock = None

        self.ui.btnSend.clicked.connect(self.send)

        self.keys = {
            'p': 1,
            'q': 2
        }

        self.preSharedKeys = {
            'p': 1,
            'q': 2
        }

    def setUser(self, user):
        self.user = user

    def setPreSharedKeys(self, pKeyP, pKeyQ):
        self.preSharedKeys['p'] = pKeyP
        self.preSharedKeys['q'] = pKeyQ
 
    def setContact(self, contact):
        self.contact = contact

    def send(self):
        self.genKeys()
        textTemp = self.ui.chatTextField.text()
        
        if textTemp == '':
            return
        
        ## Encrypt the message with the generated keys....
        cryptList = fc.fibocrypt(textTemp, self.keys['p'], self.keys['q'])

        ## Convert the fibonacci matrix to string notation, changing the keys
        ##      by subtracting them with preSharedKeys....
        print('before sending, subtracting psk: P: ' + str(self.preSharedKeys['p'])+' Q: ' + str(self.preSharedKeys['q']))
        text = fc.toString(cryptList, self.keys['p'] - self.preSharedKeys['p'], self.keys['q'] - self.preSharedKeys['q'])
        font=self.ui.chat.font()
        font.setPointSize(13)
        self.ui.chat.setFont(font)
        textFormatted='{:>80}'.format(textTemp)
        self.ui.chat.append('Me: ' + textFormatted)
        self.ui.chatTextField.setText("")

        sendObj = {
            'type': 'message',
            'touser': self.contact,
            'fromuser': self.user,
            'message': text
        }

        sendJson = json.dumps(sendObj)

        DBInit.insertMessage(self.user, self.contact, 'O', text)

        self.sock.send(bytes(sendJson, 'utf-8'))


    def receive(self, fromuser, text):
        self.ui.chat.append('{:<80}'.format(fromuser+': '+ text))

    def setSock(self, sock):
        self.sock = sock

    def loadPreviosChats(self, prevChats):
        for message in prevChats:
            if message['direction'] == 'O':
                self.ui.chat.append('Me: ' + message['text'])
            else:
                self.ui.chat.append(message['fromuser']+': '+message['text'])

    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def genKeys(self):
        ## Create a random 3-digit integer
        rndm = randomInt(3)

        self.keys['p'] = fibNo(rndm)
        self.keys['q'] = fibNo(rndm + 1)