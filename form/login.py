from PyQt5 import QtWidgets, uic
import sys

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../ui/login/login.ui', self)
        self.show()