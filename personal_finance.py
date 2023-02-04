### List of packages that need to be installed ###
## Task 1 and 3: splitwise, sqlite3, json
## Task 7: pyqt5, pyqt5-tools

### Importing all the necessary libraries ###
### For the interface ##
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from sql_queries_methods import *
from console import Ui_MainWindow
from integrated_tasks import *
from datetime import datetime
# Task 4
import unrect_transac as unrt
from Prediction_TraMy import *



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
                self.ui.UNR_submit_button.clicked.connect(self.unr_submit)

                ### Signal for Income Input ###
                self.ui.Button_Income_submit.clicked.connect(self.submit_income)
                ### Signal for Expense Input ###
                self.ui.Button_expense_submit.clicked.connect(self.submit_expense)
                ### Signal for Prediction ###
                self.ui.Button_prediction_generate.clicked.connect(self.generate_predict)
                self.ui.Button_prediction_download.clicked.connect(self.download_pdf)
                ### Signal for Reporting ###
                self.ui.Button_reporting_generate.clicked.connect(self.generate_report)
                self.ui.Button_reporting_download.clicked.connect(self.download_report)

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
                try:
                        fact = round(float(self.ui.Fact_edit.text()),2)
                except ValueError:
                        fact_err = QMessageBox()
                        fact_err.setWindowTitle("Factual balance input error")
                        fact_err.setText("Invalid factual balance amount. Please make sure to write a number")
                        fact_err.setIcon(QMessageBox.Critical)
                        fact_popup = fact_err.exec_()
                else:
                        unr, income, expense, net_debt, owes, owed = unrt.unrecorded_transaction_no_write(fact)
                        print(fact)
                        self.ui.Income_value_label.setText(str(round(income,2))+" €")
                        self.ui.Expense_value_label.setText(str(round(expense,2))+" €")
                        self.ui.Debt_value_label.setText(str(round(net_debt,2))+" €")
                        self.ui.Owe_label_value.setText(str(round(owes,2))+" €")
                        self.ui.Owed_label_value.setText(str(round(owed,2))+" €")
                        self.ui.UNR_label_2.setText("UNR Amount: "+str(round(unr,2))+" €")
        def unr_submit(self):
                try:
                        fact = round(float(self.ui.Fact_edit.text()),2)
                except ValueError:
                        fact_err = QMessageBox()
                        fact_err.setWindowTitle("Factual balance input error")
                        fact_err.setText("Invalid factual balance amount. Please make sure to write a number")
                        fact_err.setIcon(QMessageBox.Critical)
                        fact_popup = fact_err.exec_()
                else:
                        unr, income, expense, net_debt, owes, owed = unrt.unrecorded_transaction_write(fact)
                        self.ui.Income_value_label.setText(str(round(income,2))+" €")
                        self.ui.Expense_value_label.setText(str(round(expense,2))+" €")
                        self.ui.Debt_value_label.setText(str(round(net_debt,2))+" €")
                        self.ui.Owe_label_value.setText(str(round(owes,2))+" €")
                        self.ui.Owed_label_value.setText(str(round(owed,2))+" €")
                        self.ui.UNR_label_2.setText("UNR Amount: "+str(round(unr,2))+" €")
                        msg_unr = QMessageBox()
                        msg_unr.setWindowTitle("Fact Balance Confirmation")
                        msg_unr.setText("Factual Balance has been submitted successfully")
                        msg_unr.setIcon(QMessageBox.Information)
                        unr_popup = msg_unr.exec_()
                        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        ### Events for Income Submit ###
        def submit_income(self):
                conn, cursor, user_id = get_connection_cursor()
                try:
                        amount = abs(round(float(self.ui.Income_edit.text()),2))
                except ValueError:
                        amount_err = QMessageBox()
                        amount_err.setWindowTitle("Input Error")
                        amount_err.setText("Invalid amount. Please make sure to write a number")
                        amount_err.setIcon(QMessageBox.Critical)
                        err_popup = amount_err.exec_()
                else:
                        subcategory = self.ui.Income_category.currentText()
                        if subcategory == 'Choose category':
                                cat_err = QMessageBox()
                                cat_err.setWindowTitle("Category Error")
                                cat_err.setText("Please choose a valid category")
                                cat_err.setIcon(QMessageBox.Critical)
                                cat_popup = cat_err.exec_()
                        else:
                                subcategory = subcategory.split("-")[1]
                                subcategory_id = find_income_subcategory_by_name(conn,cursor,subcategory)[0]
                                transaction_date = self.ui.dateEdit_income.date()
                                transaction_date = transaction_date.toString(QtCore.Qt.DateFormat.ISODate)+"T00:00:00Z"
                                insert_transaction(conn, cursor, transaction_date, None, subcategory_id, None, 'EUR', None)
                                transaction_id = cursor.lastrowid
                                insert_transaction_item(conn, cursor, transaction_id, user_id, amount)
                                msg_inc = QMessageBox()
                                msg_inc.setWindowTitle("Income Input Confirmation")
                                msg_inc.setText("Income has been submitted successfully")
                                msg_inc.setIcon(QMessageBox.Information)
                                I_popup = msg_inc.exec_()
                                self.ui.stackedWidget.setCurrentWidget(self.ui.home)


        ### Events for Expense Submit ###
        def submit_expense(self):
                conn, cursor, user_id = get_connection_cursor()
                try:
                        amount = abs(round(float(self.ui.expense_edit.text()),2))
                except ValueError:
                       amount_err = QMessageBox()
                       amount_err.setWindowTitle("Input Error")
                       amount_err.setText("Invalid amount. Please make sure to write a number")
                       amount_err.setIcon(QMessageBox.Critical)
                       err_popup = amount_err.exec_()
                else:
                        subcategory = self.ui.expense_category.currentText()
                        if subcategory == 'Choose category':
                                cat_err = QMessageBox()
                                cat_err.setWindowTitle("Category Error")
                                cat_err.setText("Please choose a valid category")
                                cat_err.setIcon(QMessageBox.Critical)
                                cat_popup = cat_err.exec_()
                        else:
                                subcategory = subcategory.split("-")[1]
                                subcategory_id = find_expense_subcategory_by_name(conn, cursor, subcategory)[0]
                                transaction_date = self.ui.dateEdit_expense.date()
                                transaction_date = transaction_date.toString(QtCore.Qt.DateFormat.ISODate) + "T00:00:00Z"
                                insert_transaction(conn, cursor, transaction_date, None, subcategory_id, None, 'EUR', None)
                                transaction_id = cursor.lastrowid
                                insert_transaction_item(conn, cursor, transaction_id, user_id, amount)
                                msg_exp = QMessageBox()
                                msg_exp.setWindowTitle("Expense Input Confirmation")
                                msg_exp.setText("Expense has been submitted successfully")
                                msg_exp.setIcon(QMessageBox.Information)
                                E_popup = msg_exp.exec_()
                                self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        ### Buton Events for Prediction ###
        def generate_predict(self):
                bal1, bal2, bal3, predict = run_prediction()
                name, fig = plot_prediction(bal1, bal2, bal3, predict)
                save_plot_jpg(name, fig)
                self.ui.image_predict.setPixmap(QtGui.QPixmap(name+".jpg"))
        def download_pdf(self):
                bal1, bal2, bal3, predict = run_prediction()
                name, fig = plot_prediction(bal1, bal2, bal3, predict)
                download_plot(name,fig)
                msg_pred = QMessageBox()
                msg_pred.setWindowTitle("Download Confirmation")
                msg_pred.setText("The plot has been successfully downloaded as a pdf file")
                msg_pred.setIcon(QMessageBox.Information)
                E_popup = msg_pred.exec_()

        ### Button Events for Reporting ###
        def generate_report(self):
                pass

        def download_report(self):
                pass


#%%

def run_app():
    # Run task 1, task 2, task 3 #
    run_sync()
    # Initiates App ##
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

#%%
if __name__ == "__main__":
    run_app()