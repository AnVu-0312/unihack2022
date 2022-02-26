from PyQt5 import QtWidgets, uic
import sys

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
        self.show()