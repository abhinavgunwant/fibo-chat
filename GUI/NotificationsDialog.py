import re
import DBInit
import sys
import PyQt5
import GUI.MainWindowGUI
import FiboCrypt.fibocrypt as fc

from PyQt5                      import QtGui, QtWidgets
from PyQt5.QtWidgets            import QWidget, QApplication, QMainWindow, QDialog

from GUI.RegisterDialogGUI      import Ui_Register
from GUI.NotificationDialogGUI  import Ui_Dialog

class NotificationDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)