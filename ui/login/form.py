from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.QtWidgets import QTableView,QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
import os 


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        loadUi(dir_path + '\login.ui', self)
        self.show()