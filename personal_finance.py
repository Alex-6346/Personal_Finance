### List of packages that need to be installed ###
## Task 1 and 3: splitwise, sqlite3, json
## Task 7: pyqt5, pyqt5-tools

### Importing all the necessary libraries ###
from first_third_tasks import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# Running Splitwise Sync and currency process (Task 1 and 3) #
#run_sync_currency()

## Defining the Interface ##
def Personal_Finance():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(900,400,700,500)
    win.setWindowTitle("Personal Finance: A Splitwise Extension (Prototype)")

    label = QtWidgets.QLabel(win)
    label.setText("Welcome to the Finance App")
    label.move(300,50)

    win.show()
    sys.exit(app.exec_())

Personal_Finance()
