import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.QtWidgets import QTableView,QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import sqlite3 
import matplotlib.pyplot as plt
import pandas as pd 
import datetime
from datetime import datetime
import numpy as np
import xlrd
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import time

def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("csdl.db")
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
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.forgotpassword.clicked.connect(self.resetpass)
        self.quitbutton.clicked.connect(self.quit_program)
    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        #Do not let username and password leave blank
        if email == "" or password =="":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in username and password"
            msg.setText(my_message)
            x= msg.exec_() 
        else: 
            connection = sqlite3.connect("csdl.db")
            sql = "SELECT * FROM users WHERE username=\'" + email + "\' AND password=\'" + password + "\'"
            cursor = connection.execute(sql)
            list = []
            for row in cursor:
                list.append(row)
            connection.close()

            if len(list)==1:
                #msg = QMessageBox()
                #msg.setWindowTitle("Congratulation!")
                #my_message = "Successfully logged in with email: " + email 
                #msg.setText(my_message)
                #x= msg.exec_()           
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

class Resetpass(QDialog):
    def __init__(self):
        super(Resetpass,self).__init__()
        loadUi("resetpass.ui",self)
        self.newpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmnewpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.resetbutton.clicked.connect(self.resetpass)
        self.backtologinbutton.clicked.connect(self.backtologin)

    def resetpass(self):
        username = self.username.text()
        newpass = self.newpass.text()
        confirmnewpass = self.confirmnewpass.text()
        answer = self.answersafetyquestion.text()
        #Do not let data leave blank
        if username == "" or newpass =="" or confirmnewpass == "" or answer == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in required information"
            msg.setText(my_message)
            x= msg.exec_()
        else:
            if newpass == confirmnewpass:
                connection = sqlite3.connect("csdl.db")
                sql = "SELECT * FROM users WHERE username=\'" + username + "\' AND safetyquestion=\'" + answer + "\'"
                table = connection.execute(sql)
                list = []
                for row in table:
                    list.append(row)
                connection.close()
                if len(list)==1:
                    connection = sqlite3.connect("csdl.db")
                    reset = "UPDATE users SET password =\'" + newpass + "\' WHERE username=\'" + username + "\' AND safetyquestion=\'" + answer + "\'"
                    connection.execute(reset)
                    connection.commit()
                    connection.close()
                    msg = QMessageBox()
                    msg.setWindowTitle("Successfully Reset")
                    reset_message = "New password has been updated in the database"
                    msg.setText(reset_message)
                    x= msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                error_message = "New password and confirmed new password need to be identical"
                msg.setText(erorr_message)
                x= msg.exec_()
                
    def backtologin(self):
        loginback=Login()
        widget.addWidget(loginback)
        widget.setCurrentIndex(widget.currentIndex()+1)
      
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backtologinbutton.clicked.connect(self.backtologin)
        
    def createaccfunction(self):
        email = self.email.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        safetyquestion = self.safetyquestion.text()
        
        if email == "" or password =="" or confirmpass =="" or safetyquestion == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            my_message = "Please fill in username, password, confirmed password, and safety question"
            msg.setText(my_message)
            x= msg.exec_() 
        else: 
            if self.password.text()==self.confirmpass.text():
                #checking username availability in database
                connection = sqlite3.connect("csdl.db")
                query = "SELECT * from users WHERE username =\'" + email+ "\'"
                table = connection.execute(query)
                list = []
                for row in table:
                    list.append(row)
                connection.close()

                if len(list)==1: 
                    msg = QMessageBox()
                    msg.setWindowTitle("Fail to creat an account!")
                    my_message = "The chosen username ID has already existed. Please try another name" 
                    msg.setText(my_message)
                    x= msg.exec_()

                else: 
                    connection = sqlite3.connect("csdl.db")
                    sql = "INSERT INTO users(username, password,safetyquestion) VALUES (\'" + email + "\', \'" + password + "\',\'" + safetyquestion + "\' )"
                    connection.execute(sql)
                    connection.commit()
                    connection.close()

                    msg = QMessageBox()
                    msg.setWindowTitle("Congratulation!")
                    my_message = "Successfully created account with email: " + email 
                    msg.setText(my_message)
                    x= msg.exec_()
                    login=Login()
                    widget.addWidget(login)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Failed attempt!")
                my_message = "\"Confirmed Password\" should be identical to \"Password\"!"
                msg.setText(my_message)
                x= msg.exec_()
                #self.email.clear()
                self.password.clear()
                self.confirmpass.clear()

    def backtologin(self):
        loginback=Login()
        widget.addWidget(loginback)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("mainwindow.ui",self)
        self.update()
        self.importbutton.clicked.connect(self.import_data)
        self.updatebutton.clicked.connect(self.update_data)
        self.analysebutton.clicked.connect(self.analyse_data)
        self.quitbutton.clicked.connect(self.quit_program)
    
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
        #self.adddata=AddData()
        #self.adddata.show()
        adddata=AddData()
        widget.addWidget(adddata)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def analyse_data(self):
        analysedata=AnalyseData()
        widget.addWidget(analysedata)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def quit_program(self):        
        sys. exit() 

class AddData(QMainWindow):    
    def __init__(self):
        super(AddData,self).__init__()
        loadUi("adddata.ui",self)
        self.count = 0
        self.addincomebutton.clicked.connect(self.add_income)
        self.addcostbutton.clicked.connect(self.add_cost)
        #self.showincomebutton.clicked.connect(self.show_income)
        #self.showcostbutton.clicked.connect(self.show_cost)
        self.backbutton.clicked.connect(self.back_window)

    def add_income(self):
        self.setWindowTitle("Add income interface")
        self.count = self.count + 1 # this is incrementing counter
        
        currentDay = str(datetime.now().day)
        if len(currentDay)==1:
            currentDay = '0'+currentDay
        currentMonth = str(datetime.now().month)
        if len(currentMonth)==1:
            currentMonth = '0'+currentMonth
        currentYear = str(datetime.now().year)

        date = self.date.text()
        income = self.income.text()
        incometype = self.incometype.currentText()
        if self.date.text()!="" and self.income.text()!="":
            try :
                getdate = datetime.strptime(date, "%d/%m/%Y")
                
                inputDay = str(getdate.day)
                if len(inputDay)==1:
                    inputDay = '0'+inputDay
                inputMonth = str(getdate.month)
                if len(inputMonth)==1:
                    inputMonth = '0'+inputMonth
                inputYear = str(getdate.year)
                
                sql_type_date = inputYear + '-' + inputMonth + '-' + inputDay 
                connection = sqlite3.connect("csdl.db")
                sql = "INSERT INTO incomes(date, income, incometype) VALUES (\'" + sql_type_date + "\', \'" + income + "\', \'" + incometype + "\')"
                connection.execute(sql)
                connection.commit()
                connection.close()
                self.showincome=ShowIncome()
                self.showincome.show()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Failed attempt!")
                my_message = "Error: Date inputted must be in format dd/mm/yyyy. Current date will be suggested as an example " 
                msg.setText(my_message)
                x= msg.exec_()

                currentDMY = currentDay + '/'+ currentMonth + '/' + currentYear
                self.date.setText(currentDMY)    
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "Input value for " 
            if self.date.text()=="":
                my_message += " \"Date\" "
            if self.income.text()=="":
                my_message += " \"Income\" "
            if self.incometype.text()=="":
                my_message += " \"Income Type\" " 
            msg.setText(my_message)
            x= msg.exec_()     

        #self.editdata=EditData()
        #self.editdata.show()
             
    def add_cost(self):
        self.setWindowTitle("Add cost interface")
        self.count = self.count + 1 # this is incrementing counter
        
        currentDay = str(datetime.now().day)
        if len(currentDay)==1:
            currentDay = '0'+currentDay
        currentMonth = str(datetime.now().month)
        if len(currentMonth)==1:
            currentMonth = '0'+currentMonth
        currentYear = str(datetime.now().year)

        date = self.date.text()
        cost = self.cost.text()
        costtype = self.costtype.currentText()
        if self.date.text()!="" and self.cost.text()!="":
            try :
                getdate = datetime.strptime(date, "%d/%m/%Y")
                
                inputDay = str(getdate.day)
                if len(inputDay)==1:
                    inputDay = '0'+inputDay
                inputMonth = str(getdate.month)
                if len(inputMonth)==1:
                    inputMonth = '0'+inputMonth
                inputYear = str(getdate.year)
                
                sql_type_date = inputYear + '-' + inputMonth + '-' + inputDay 
                connection = sqlite3.connect("csdl.db")
                sql = "INSERT INTO costs(date, cost, costtype) VALUES (\'" + sql_type_date + "\', \'" + cost + "\', \'" + costtype + "\')"
                connection.execute(sql)
                connection.commit()
                connection.close()
                self.showcost=ShowCost()
                self.showcost.show()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("Failed attempt!")
                my_message = "Error: Date inputted must be in format dd/mm/yyyy. Current date will be suggested as an example " 
                msg.setText(my_message)
                x= msg.exec_()

                currentDMY = currentDay + '/'+ currentMonth + '/' + currentYear
                self.date.setText(currentDMY)    

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Failed attempt!")
            my_message = "Input value for " 
            if self.date.text()=="":
                my_message += " \"Date\" "
            if self.cost.text()=="":
                my_message += " \"Cost\" "
            if self.costtype.text()=="":
                my_message += " \"Cost Type\" " 
            msg.setText(my_message)
            x= msg.exec_()    
        #self.editdata=EditData()
        #self.editdata.show()

    def show_income(self):
        self.showincome=ShowIncome()
        self.showincome.show()

    def show_cost(self):
        self.showcost=ShowCost()
        self.showcost.show()
    
    def back_window(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)            

class AnalyseData(QMainWindow):    
    def __init__(self):
        super(AnalyseData,self).__init__()
        loadUi("analysedata.ui",self)
        self.incomemonthbutton.clicked.connect(self.income_bymonth)
        self.incometypebutton.clicked.connect(self.income_bytype)
        self.costmonthbutton.clicked.connect(self.cost_bymonth)
        self.costtypebutton.clicked.connect(self.cost_bytype)
        self.incomecostbutton.clicked.connect(self.compare_incomecost)
        self.backbutton.clicked.connect(self.back_window)
        
    def income_bymonth(self):
        def on_pick_bar(event):
            circle1 = plt.Circle((0, 0), 0.1, color='blue', fill=True)
            fig = plt.gcf()
            ax = fig.gca()
            ax.add_patch(circle1)
            income_index_to_analyse = int(round(event.artist.xy[0]))-1
            income_month_to_analyse = income_labels[income_index_to_analyse]
            plt.gca().set_title("Income over months!\n(You have just chosen to further analyse this month: "+ income_month_to_analyse+")")
            self.income_bytype_1month(income_month_to_analyse)

        connection = sqlite3.connect("csdl.db")
        sql = "SELECT strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(income) FROM incomes GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date) "
        cursor = connection.execute(sql)
        # x-coordinates of left sides of bars
        left = []
        # heights of bars
        income_values = []
        # labels of bars
        income_labels =[]
        index = 0
        for row in cursor:
            index += 1
            left.append(index)
            income_labels.append(row[0])
            income_values.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        fig.autofmt_xdate(rotation=(min(90,index/12*45)))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.bar(left, income_values, tick_label = income_labels, width = 0.8, color = ['red', 'green'], picker = True) 
        ax.set_title('Income over months!\nClick on a month to further analyse the income of that month by type.')
        ax.set_xlabel('Months')
        ax.set_ylabel('Income')
        fig.canvas.callbacks.connect('pick_event',on_pick_bar)

    def income_bymonth_1type(self, income_type_to_analyse):
        connection = sqlite3.connect("csdl.db")
        sql = "SELECT strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(income) FROM incomes WHERE incometype=\'"+income_type_to_analyse+"\' GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date) "
        cursor = connection.execute(sql)
        # x-coordinates of left sides of bars
        left = []
        # heights of bars
        income_values = []
        # labels of bars
        income_labels =[]
        index = 0
        for row in cursor:
            index += 1
            left.append(index)
            income_labels.append(row[0])
            income_values.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        fig.autofmt_xdate(rotation=(min(90,index/12*45)))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.bar(left, income_values, tick_label = income_labels, width = 0.8, color = ['red', 'green'], picker = True) 
        ax.set_title('Income over months of the activity '+income_type_to_analyse+ '\n(Close this window to return to the analysis of Income by type)')
        ax.set_xlabel('Months')
        ax.set_ylabel('Income')

    def income_bytype(self):
        def on_pick_slide(event):
            if event.inaxes!=my_ax:
                return
            for w in ax_instance[0]:
                (hit,_) = w.contains(event)
                if hit:
                    income_type_to_analyse = w.get_label()
                    circle1 = plt.Circle((event.x, event.y), 0.1, color='black', fill=True)
                    fig = plt.gcf()
                    ax = fig.gca()
                    ax.add_patch(circle1)
                    plt.gca().set_title("Income from different activities!\n(You have just chosen to further analyse this activity: "+ income_type_to_analyse+")")
                    self.income_bymonth_1type(income_type_to_analyse) 
        
        connection = sqlite3.connect("csdl.db")
        #defining portions and labels covered
        sql = "SELECT SUM(income), incometype FROM incomes GROUP BY incometype ORDER BY SUM(income) DESC"
        cursor = connection.execute(sql)
        slices = []
        types = []
        for row in cursor:
            slices.append(row[0])
            types.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_title('Income from different activities!\nClick on an activity to further analyse the income of that activity by month.')
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
        ax_instance = ax.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%') 

        my_fig = ax_instance[0][0].figure
        my_ax = ax_instance[0][0].axes
        income_type_to_analyse =''            
        fig.canvas.mpl_connect('button_press_event', on_pick_slide)

    def income_bytype_1month(self, income_month_to_analyse):      
        connection = sqlite3.connect("csdl.db")
        #defining portions and labels covered
        month_part = income_month_to_analyse[0:2]
        year_part = income_month_to_analyse[3:5]
        sql = "SELECT SUM(income), incometype FROM incomes WHERE strftime('%m',date)=\'"+ month_part + "\' AND substr(strftime('%Y',date),3,2)=\'" +year_part+ "\' GROUP BY incometype ORDER BY SUM(income) DESC"
        cursor = connection.execute(sql)
        slices = []
        types = []
        for row in cursor:
            slices.append(row[0])
            types.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_title('Income from different activities of the month '+str(income_month_to_analyse)+ '\n(Close this window to return to the analysis of Income over months)')
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
        ax.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%') 
        
    def cost_bymonth(self):
        def on_pick_bar(event):
            circle1 = plt.Circle((0, 0), 0.1, color='blue', fill=True)
            fig = plt.gcf()
            ax = fig.gca()
            ax.add_patch(circle1)
            cost_index_to_analyse = int(round(event.artist.xy[0]))-1
            cost_month_to_analyse = cost_labels[cost_index_to_analyse]
            plt.gca().set_title("Costs over months!\n(You have just chosen to further analyse this month: "+ cost_month_to_analyse+")")
            self.cost_bytype_1month(cost_month_to_analyse)

        connection = sqlite3.connect("csdl.db")
        sql = "SELECT strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(cost) FROM costs GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date) "
        cursor = connection.execute(sql)
        # x-coordinates of left sides of bars
        left = []
        # heights of bars
        cost_values = []
        # labels of bars
        cost_labels =[]
        index = 0
        for row in cursor:
            index += 1
            left.append(index)
            cost_labels.append(row[0])
            cost_values.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        fig.autofmt_xdate(rotation=(min(90,index/12*45)))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.bar(left, cost_values, tick_label = cost_labels, width = 0.8, color = ['red', 'green'], picker = True) 
        ax.set_title('Costs over months!\nClick on a month to further analyse the cost of that month by type.')
        ax.set_xlabel('Months')
        ax.set_ylabel('Cost')
        fig.canvas.callbacks.connect('pick_event',on_pick_bar)

    def cost_bymonth_1type(self, cost_type_to_analyse):
        connection = sqlite3.connect("csdl.db")
        sql = "SELECT strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(cost) FROM costs WHERE costtype=\'"+cost_type_to_analyse+"\' GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date) "
        cursor = connection.execute(sql)
        # x-coordinates of left sides of bars
        left = []
        # heights of bars
        cost_values = []
        # labels of bars
        cost_labels =[]
        index = 0
        for row in cursor:
            index += 1
            left.append(index)
            cost_labels.append(row[0])
            cost_values.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        fig.autofmt_xdate(rotation=(min(90,index/12*45)))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.bar(left, cost_values, tick_label = cost_labels, width = 0.8, color = ['red', 'green'], picker = True) 
        ax.set_title('Cost over months of the activity '+cost_type_to_analyse+ '\n(Close this window to return to the analysis of Costs by type)')
        ax.set_xlabel('Months')
        ax.set_ylabel('Cost')

    def cost_bytype(self):
        def on_pick_slide(event):
            if event.inaxes!=my_ax:
                return
            for w in ax_instance[0]:
                (hit,_) = w.contains(event)
                if hit:
                    cost_type_to_analyse = w.get_label()
                    circle1 = plt.Circle((event.x, event.y), 0.1, color='black', fill=True)
                    fig = plt.gcf()
                    ax = fig.gca()
                    ax.add_patch(circle1)
                    plt.gca().set_title("Costs from different activities!\n(You have just chosen to further analyse this activity: "+ cost_type_to_analyse+")")
                    self.cost_bymonth_1type(cost_type_to_analyse) 
        
        connection = sqlite3.connect("csdl.db")
        #defining portions and labels covered
        sql = "SELECT SUM(cost), costtype FROM costs GROUP BY costtype ORDER BY SUM(cost) DESC"
        cursor = connection.execute(sql)
        slices = []
        types = []
        for row in cursor:
            slices.append(row[0])
            types.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_title('Costs from different activities!\nClick on an activity to further analyse the cost of that activity by month.')
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
        ax_instance = ax.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%') 

        my_fig = ax_instance[0][0].figure
        my_ax = ax_instance[0][0].axes
        cost_type_to_analyse =''            
        fig.canvas.mpl_connect('button_press_event', on_pick_slide)

    def cost_bytype_1month(self, cost_month_to_analyse):      
        connection = sqlite3.connect("csdl.db")
        #defining portions and labels covered
        month_part = cost_month_to_analyse[0:2]
        year_part = cost_month_to_analyse[3:5]
        sql = "SELECT SUM(cost), costtype FROM costs WHERE strftime('%m',date)=\'"+ month_part + "\' AND substr(strftime('%Y',date),3,2)=\'" +year_part+ "\' GROUP BY costtype ORDER BY SUM(cost) DESC"
        cursor = connection.execute(sql)
        slices = []
        types = []
        for row in cursor:
            slices.append(row[0])
            types.append(row[1])
        connection.close()

        plt.ion()
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_title('Cost from different activities of the month '+str(cost_month_to_analyse)+ '\n(Close this window to return to the analysis of Costs over months)')
        explode_list = []
        start_value = 0
        for i in range(0,len(slices)):
            explode_list.append(start_value)
            start_value += 0.025
        ax.pie(slices, labels = types, colors=None, startangle=0, shadow = False, explode = explode_list, radius = 1, autopct = '%1.1f%%') 
     
    def compare_incomecost(self):
        connection = sqlite3.connect("csdl.db")
        
        # preparing aggregated income values
        sql = "SELECT cast(strftime('%Y',date) as interger)*12+cast(strftime('%m',date) as interger), strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(income) FROM incomes GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date)"
        cursor = connection.execute(sql)
        income_index = []
        income_values = []
        income_labels = []
        for row in cursor:
            income_index.append(row[0])
            income_labels.append(row[1])
            income_values.append(row[2])
        # preparing aggregated cost values
        sql = "SELECT cast(strftime('%Y',date) as interger)*12+cast(strftime('%m',date) as interger), strftime('%m',date)||'-'||substr(strftime('%Y',date),3,2), SUM(cost) FROM costs GROUP BY strftime('%m-%Y',date) ORDER BY strftime('%Y',date), strftime('%m',date)"
        cursor = connection.execute(sql)
        cost_index = []
        cost_values = []
        cost_labels = []
        for row in cursor:
            cost_index.append(row[0])
            cost_labels.append(row[1])
            cost_values.append(row[2])
        connection.close()
        comparion_index = list(set(income_index + cost_index))
        comparion_index.sort()
        comparion_income = [0]*len(comparion_index)
        comparion_cost = [0]*len(comparion_index)
        comparion_label = ['']*len(comparion_index)
        plt_index = []
        for i in range(len(comparion_index)):
            plt_index = plt_index + [i]
            for j in range(len(income_values)):
                if  comparion_index[i]== income_index[j]:
                    comparion_income[i] = income_values[j]
                    comparion_label[i] = income_labels[j]
            for k in range(len(cost_values)):
                if  comparion_index[i]== cost_index[k]:
                    comparion_cost[i] = cost_values[k]
                    comparion_label[i] = cost_labels[k]
        plotdata = pd.DataFrame({'Income': comparion_income, 'Cost': comparion_cost})    
        plotdata.plot(kind="bar")
        plt.title("Income versus Cost")
        plt.xlabel("Months")
        plt.ylabel("Income/Cost values")
        plt.xticks(ticks = plt_index, labels=comparion_label, rotation=(min(90,len(comparion_index)/12*45)))
        
        # showing the plot 
        plt.ion()
        plt.show()

    def back_window(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1) 

class ShowIncome(QMainWindow):    
    def __init__(self):
        super(ShowIncome,self).__init__()
        self.load_initial_data()

    def load_initial_data(self):
        self.setWindowTitle("Show Income")
        self.resize(250, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(3)
        self.view.setHorizontalHeaderLabels(["Month", "Income", "Income Type"])
        query = QSqlQuery("SELECT date, income, incometype FROM incomes")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
            self.view.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)

class ShowCost(QMainWindow):    
    def __init__(self):
        super(ShowCost,self).__init__()
        self.load_initial_data()

    def load_initial_data(self):
        self.setWindowTitle("Show Cost")
        self.resize(250, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(3)
        self.view.setHorizontalHeaderLabels(["Month", "Cost", "Cost Type"])
        query = QSqlQuery("SELECT date, cost, costtype FROM costs")
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
            self.view.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


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
widget.setFixedWidth(510)
widget.setFixedHeight(650)
widget.show()
app.exec_()
