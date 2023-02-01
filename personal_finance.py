### List of packages that need to be installed ###
## Task 1 and 3: splitwise, sqlite3, json
## Task 7: pyqt5, pyqt5-tools

### Importing all the necessary libraries ###
from integrated_tasks import *
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from console import Ui_MainWindow


# Running Splitwise Sync and currency process (Task 1 and 3) #
#Task 1#
#run_sync()
#Task 3#

### Defining the Interface ###

## Main Window ##
class MainWindow:
        def __init__(self):
                self.main_win = QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.main_win)

                self.ui.stackedWidget.setCurrentWidget(self.ui.home)

                ### Signal of Buttons of Main Menu ###
                self.ui.Button_Income.clicked.connect(self.go_to_income)
                self.ui.Button_Expense.clicked.connect(self.go_to_expense)
                self.ui.Button_prediction.clicked.connect(self.go_to_prediction)
                self.ui.Button_reporting.clicked.connect(self.go_to_reporting)
                self.ui.Button_Unrecorded.clicked.connect(self.go_to_unrecorded)

                ### Signal of Back Buttons ###
                self.ui.Button_back.clicked.connect(self.go_to_home)
                self.ui.Button_back_2.clicked.connect(self.go_to_home)
                self.ui.Button_back_3.clicked.connect(self.go_to_home)
                self.ui.Button_back_4.clicked.connect(self.go_to_home)
                self.ui.Button_back_5.clicked.connect(self.go_to_home)

        def show(self):
                self.main_win.show()

        ### Event of Buttons of Main Menu ###
        def go_to_income(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.income)

        def go_to_expense(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.expense)

        def go_to_prediction(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.prediction)

        def go_to_reporting(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.reporting)

        def go_to_unrecorded(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.unr)

        ### Event of Back Buttons ###
        def go_to_home(self):
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)


def run_app():
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.show()
        sys.exit(app.exec_())


run_app()