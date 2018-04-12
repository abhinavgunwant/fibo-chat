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

# from GUI.RegisterDialogGUI      import Ui_Register
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtCore               import QCoreApplication
from GUI.MainWindow             import MainWindow
from GUI.ChatDialogGUI          import Ui_Chat
from FiboCrypt.fibocrypt        import fibocrypt, toString

# app             = QApplication(sys.argv)
# signInDialog    = SignInDialog()

class ChatDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Chat()
        # self.ui.setupUi(self)

        self.touser = None
        self.fromuser = None
        self.sock = None

        self.ui.btnSend.clicked.connect(self.send)

    def setTouser(self, touser):
        self.touser = touser
 
    def setFromuser(self, fromuser):
        self.fromuser = fromuser

    def send(self):
        text=self.ui.chatTextField.text()
        font=self.ui.chat.font()
        font.setPointSize(13)
        self.ui.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.ui.chat.append(textFormatted)
        # tcpClientA.send(text.encode())
        self.ui.chatTextField.setText("")

        sendObj = {
            'type': 'message',
            'touser': self.touser,
            'fromuser': self.fromuser,
            'message': text
        }

        sendJson = json.dumps(sendObj)

        self.sock.send(bytes(sendJson, 'utf-8'))


    def receive(self, fromuser, text):
        self.ui.chat.append(fromuser+': '+ text)

    def setSock(self, sock):
        self.sock = sock

    def showMessage(self,title,msg):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()