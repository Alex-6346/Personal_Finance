### List of packages that need to be installed ###
## Task 1 and 3: splitwise, sqlite3, json
## Task 7: pyqt5, pyqt5-tools

### Importing all the necessary libraries ###
from first_third_tasks import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# Running Splitwise Sync and currency process (Task 1 and 3) #
#run_sync_currency()

## Defining the Interface ##

class Ui_Menu(object):
    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(760, 631)
        font = QtGui.QFont()
        font.setPointSize(12)
        Menu.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.AppTitle = QtWidgets.QLabel(self.centralwidget)
        self.AppTitle.setGeometry(QtCore.QRect(140, 20, 481, 131))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.AppTitle.setFont(font)
        self.AppTitle.setObjectName("AppTitle")
        self.Income = QtWidgets.QPushButton(self.centralwidget)
        self.Income.setGeometry(QtCore.QRect(280, 190, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Income.setFont(font)
        self.Income.setObjectName("Income")
        self.Unrecorded = QtWidgets.QPushButton(self.centralwidget)
        self.Unrecorded.setGeometry(QtCore.QRect(150, 370, 461, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Unrecorded.setFont(font)
        self.Unrecorded.setObjectName("Unrecorded")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 280, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.Reporting = QtWidgets.QPushButton(self.centralwidget)
        self.Reporting.setGeometry(QtCore.QRect(400, 280, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Reporting.setFont(font)
        self.Reporting.setObjectName("Reporting")
        Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 760, 44))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Menu)
        self.statusbar.setObjectName("statusbar")
        Menu.setStatusBar(self.statusbar)
        self.actionUser = QtWidgets.QAction(Menu)
        self.actionUser.setObjectName("actionUser")
        self.actionIncome_Input = QtWidgets.QAction(Menu)
        self.actionIncome_Input.setObjectName("actionIncome_Input")
        self.actionPrediction = QtWidgets.QAction(Menu)
        self.actionPrediction.setObjectName("actionPrediction")
        self.actionReporting = QtWidgets.QAction(Menu)
        self.actionReporting.setObjectName("actionReporting")
        self.actionUnrecorded_transactions = QtWidgets.QAction(Menu)
        self.actionUnrecorded_transactions.setObjectName("actionUnrecorded_transactions")
        self.actionExit = QtWidgets.QAction(Menu)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionIncome_Input)
        self.menuMenu.addAction(self.actionPrediction)
        self.menuMenu.addAction(self.actionReporting)
        self.menuMenu.addAction(self.actionUnrecorded_transactions)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        _translate = QtCore.QCoreApplication.translate
        Menu.setWindowTitle(_translate("Peprsonal Finance", "Personal Finance"))
        self.AppTitle.setText(_translate("Menu", "Personal Finance"))
        self.Income.setText(_translate("Menu", "Income Input"))
        self.Unrecorded.setText(_translate("Menu", "Unrecorded transactions"))
        self.pushButton.setText(_translate("Menu", "Prediction"))
        self.Reporting.setText(_translate("Menu", "Reporting"))
        self.menuMenu.setTitle(_translate("Menu", "Menu"))
        self.actionUser.setText(_translate("Menu", "User"))
        self.actionIncome_Input.setText(_translate("Menu", "Income Input"))
        self.actionPrediction.setText(_translate("Menu", "Prediction"))
        self.actionReporting.setText(_translate("Menu", "Reporting"))
        self.actionUnrecorded_transactions.setText(_translate("Menu", "Unrecorded transactions"))
        self.actionExit.setText(_translate("Menu", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Menu = QtWidgets.QMainWindow()
    ui = Ui_Menu()
    ui.setupUi(Menu)
    Menu.show()
    sys.exit(app.exec_())
