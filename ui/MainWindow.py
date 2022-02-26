import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("ui\main.ui",self)
        self.actionQuit.triggered.connect(self.quit)
    def quit(self): 
        sys.exit()