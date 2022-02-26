import sys
from PyQt5.QtWidgets import QApplication
from ui.login.form import Login


app = QApplication(sys.argv)
window = Login()
app.exec_()