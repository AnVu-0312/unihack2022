import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.QtWidgets import QTableView,QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import sqlite3

from ui.MainWindow import MainWindow


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("db\csdl.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("ui\login\login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.forgotpassword.clicked.connect(self.resetpass)
        self.quitbutton.clicked.connect(self.quit_program)
        
    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        #Do not let username and password leave blank
        if username == "" or password =="":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in username and password"
            msg.setText(my_message)
            x= msg.exec_() 
        else: 
            connection = sqlite3.connect("db/csdl.db")
            sql = "SELECT * FROM users WHERE username=\'" + username + "\' AND password=\'" + password + "\'"
            cursor = connection.execute(sql)
            list = []
            for row in cursor:
                list.append(row)
            connection.close()

            if len(list)==1:        
                mainwindow = MainWindow()
                widget.addWidget(mainwindow)
                widget.setCurrentIndex(widget.currentIndex()+1)            
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Failed attempt!")
                my_message = "Please check your username and password" 
                msg.setText(my_message)
                x= msg.exec_()

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def resetpass(self):
        resetpass = Resetpass()
        widget.addWidget(resetpass)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def quit_program(self):        
        sys. exit() 

app = QApplication(sys.argv)
if not createConnection():
    msg = QMessageBox()
    msg.setWindowTitle("Error in opening data source!")
    my_message = "Could not open the data source. The program wil be closed! "  
    msg.setText(my_message)
    x= msg.exec_()
    sys.exit(1)

logindialog = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(logindialog)
widget.setFixedWidth(600)
widget.setFixedHeight(550)
widget.show()
app.exec_()
