import sys
import PyQt5
import GUI.MainWindowGUI

from PyQt5              import QtGui, QtWidgets
from PyQt5.QtWidgets    import QWidget, QApplication, QMainWindow
from GUI.MainWindowGUI  import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
