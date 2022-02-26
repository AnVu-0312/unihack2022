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

class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("mainwindow.ui",self)
        self.update()
        self.actionQuit.triggered.connect(self.Quit)
        self.actionImportExcelFile.triggered.connect(self.ImportExcelFile)
        self.actionInputIncome_2.triggered.connect(self.InputIncome)
        self.actionInputExpense_2.triggered.connect(self.InputExpense)
        self.actionInput_Expected_Saving.triggered.connect(self.Input_Expected_Saving)
    
    def update(self):
        connection = sqlite3.connect("csdl.db")
        
        sql = "select sum(income) from incomes"
        cursor = connection.execute(sql)
        total_income = cursor.fetchall()[0][0]
        sql = "select sum(cost) from costs"
        cursor = connection.execute(sql)
        total_cost = cursor.fetchall()[0][0]
        total_balance = total_income - total_cost
        if total_balance<0:
            total_balance = - total_balance
            self.totalvaluelabel.setText('-$'+ str(total_balance))
        else:
            self.totalvaluelabel.setText('$'+ str(total_balance))

        sql = "select sum(income) from incomes where date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')"
        cursor = connection.execute(sql)
        thismonth_income = cursor.fetchall()[0][0]
        self.thismonthincomelabel.setText('Income: $'+ str(thismonth_income))

        sql = "select sum(cost) from costs where date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')"
        cursor = connection.execute(sql)
        thismonth_cost = cursor.fetchall()[0][0]
        self.thismonthcostlabel.setText('Costs: -$'+ str(thismonth_cost))

        sql = "select sum(income) from incomes where date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')"
        cursor = connection.execute(sql)
        thisweek_income = cursor.fetchall()[0][0]
        self.thisweekincomelabel.setText('Income: $'+ str(thisweek_income))

        sql = "select sum(cost) from costs where date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')"
        cursor = connection.execute(sql)
        thisweek_cost = cursor.fetchall()[0][0]
        self.thisweekcostlabel.setText('Costs: -$'+ str(thisweek_cost))

    def import_data(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window

        currdir = os.getcwd()
        chosenfile = askopenfilename(parent=root, initialdir=currdir, title='Please select a .xls file')
        if not chosenfile:
            msg = QMessageBox()
            msg.setWindowTitle("Error!")
            my_message = "No file selected!" 
            msg.setText(my_message)
            x= msg.exec_()
        else:
            if chosenfile.endswith('.xls'): 
                my_message = "Importing information: "
                if len(chosenfile) > 0:      
                    book = xlrd.open_workbook(chosenfile)
                connection = sqlite3.connect("csdl.db")

                try:
                    cursor = connection.cursor()
                    sheet = book.sheet_by_name("Incomes")
                except :
                    my_message = my_message + "\n The Excel file has no Incomes sheet" 
                else:        
                    for r in range(1, sheet.nrows):
                        date = sheet.cell(r,0).value
                        income = sheet.cell(r,1).value
                        incometype = sheet.cell(r,2).value
                        sql = "INSERT INTO incomes (date, income, incometype) VALUES (\'" + str(date) + "\',\'" + str(income) + "\',\'" + str(incometype) + "\')"
                        cursor = connection.execute(sql)
                    Income_columns = str(sheet.ncols)
                    Income_rows = str(sheet.nrows-1)
                    my_message = my_message + "\n Incomes: " + Income_columns + " columns, " + Income_rows + " rows! "
                    cursor.close()

                try:
                    cursor = connection.cursor()
                    sheet = book.sheet_by_name("Costs")
                except :
                    my_message = my_message + "\n The Excel file has no Costs sheet" 
                else:
                    for r in range(1, sheet.nrows):
                        date = sheet.cell(r,0).value
                        cost = sheet.cell(r,1).value
                        costtype = sheet.cell(r,2).value
                        sql = "INSERT INTO costs (date, cost, costtype) VALUES (\'" + str(date) + "\',\'" + str(cost) + "\',\'" + str(costtype) + "\')"
                        cursor = connection.execute(sql)
                    Cost_columns = str(sheet.ncols)
                    Cost_rows = str(sheet.nrows-1)
                    my_message = my_message + "\n Costs: " + Cost_columns + " columns, " + Cost_rows + " rows! "
                    cursor.close()
                connection.commit()
                connection.close()
            
                msg = QMessageBox()
                msg.setWindowTitle("Task is done!")
                msg.setText(my_message)
                x= msg.exec_()
            
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error!")
                my_message = "File selected is not a .xls file!" 
                msg.setText(my_message)
                x= msg.exec_()


    def update_data(self):
        adddata=AddData()
        widget.addWidget(adddata)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def analyse_data(self):
        analysedata=AnalyseData()
        widget.addWidget(analysedata)
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
