import sys
import PyQt5
import GUI.MainWindowGUI

from PyQt5                      import QtGui, QtWidgets
from PyQt5.QtWidgets            import QWidget, QApplication, QMainWindow, QDialog
from GUI.RegisterDialogGUI      import Ui_Register

class RegisterDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Register()
        self.ui.setupUi(self)
