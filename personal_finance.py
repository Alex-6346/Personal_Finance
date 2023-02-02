### List of packages that need to be installed ###
## Task 1 and 3: splitwise, sqlite3, json
## Task 7: pyqt5, pyqt5-tools

### Importing all the necessary libraries ###
### For the interface ##
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

from PersonalFinance_Group5_Presentation.sql_queries_methods import find_income_subcategory_by_name, \
        get_connection_cursor, insert_transaction, insert_transaction_item, find_expense_subcategory_by_name
from console import Ui_MainWindow
## Task 3 ##
from sql_currency import currency

from integrated_tasks import *
from datetime import datetime


#from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
#from second_task import sql_income
#import unrect_transac as unrt



# Running Splitwise Sync and currency process (Task 1 and 3) #
# Task 1 #
run_sync()
#Task 3#
#run_currency()
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

                ### Signal of Buttons of UNR transactions ###
                self.ui.UNR_calculate_button.clicked.connect(self.unr_calculate)

                ### Signal for Income Input ###
                self.ui.Button_Income_submit.clicked.connect(self.submit_income)
                ### Signal for Expense Input ###
                self.ui.Button_expense_submit.clicked.connect(self.submit_expense)

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

        ### Button evens in UNR ###
        def unr_calculate(self):
                fact = int(self.ui.Fact_edit.text())
                unr, income, expense, debt, owes, owed = unrt.unrecorded_transaction_write(sObj, fact)
                self.ui.Income_value_label.setText(str(income))
                self.ui.Expense_value_label.setText(str(expense))
                self.ui.Debt_value_label.setText(str(debt))
                self.ui.Owe_label_value.setText(str(owes))
                self.ui.Owed_label_value.setText(str(owed))
                self.ui.UNR_label_2.setText("UNR Amount: "+str(unr))

        ### Events for Income Submit ###
        def submit_income(self):
                conn, cursor, user_id = get_connection_cursor()
                amount = int(self.ui.Income_edit.text())
                print(amount)
                subcategory = self.ui.Income_category.currentText()
                subcategory = subcategory.split("-")[1]
                print(subcategory)
                subcategory_id = find_income_subcategory_by_name(conn,cursor,subcategory)[0]
                print(subcategory_id)
                transaction_date = self.ui.dateEdit_income.date()
                transaction_date = transaction_date.toString(QtCore.Qt.DateFormat.ISODate)+"T00:00:00Z"
                print(transaction_date)

                insert_transaction(conn, cursor, transaction_date, None, subcategory_id, None, 'EUR', None)
                transaction_id = cursor.lastrowid
                insert_transaction_item(conn, cursor, transaction_id, user_id, amount)
                print("done!")
                msg_inc = QMessageBox()
                msg_inc.setWindowTitle("Income Input Confirmation")
                msg_inc.setText("Income has been submitted successfully")
                I_popup = msg_inc.exec_()
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)


        ### Events for Expense Submit ###
        def submit_expense(self):
                conn, cursor, user_id = get_connection_cursor()
                amount = int(self.ui.expense_edit.text())
                print(amount)
                subcategory = self.ui.expense_category.currentText()
                subcategory = subcategory.split("-")[1]
                print(subcategory)
                subcategory_id = find_expense_subcategory_by_name(conn, cursor, subcategory)[0]
                print(subcategory_id)
                transaction_date = self.ui.dateEdit_expense.date()
                transaction_date = transaction_date.toString(QtCore.Qt.DateFormat.ISODate) + "T00:00:00Z"
                print(transaction_date)

                insert_transaction(conn, cursor, transaction_date, None, subcategory_id, None, 'EUR', None)
                transaction_id = cursor.lastrowid
                insert_transaction_item(conn, cursor, transaction_id, user_id, amount)
                print("done!")
                msg_exp = QMessageBox()
                msg_exp.setWindowTitle("Expense Input Confirmation")
                msg_exp.setText("Expense has been submitted successfully")
                E_popup = msg_exp.exec_()
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)
def run_app():
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.show()
        sys.exit(app.exec_())


run_app()