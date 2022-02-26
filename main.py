from PyQt5 import QtWidgets, uic

import sys
sys.path.append("ui/login/form.py") 
from ui.login.form import Login


app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec_()