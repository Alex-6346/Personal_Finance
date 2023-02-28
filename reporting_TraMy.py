import sqlite3
import pandas as pd

try:
    sqliteConnect = sqlite3.connect("61730143.sqlite")
    cursor = sqliteConnect.cursor()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


try:

    query = '''
        SELECT * FROM Transactions AS t
        INNER JOIN TransactionItems AS ti
            ON t.id = ti.transaction_id
        INNER JOIN Subcategories as s
            ON s.id = t.subcategory_id
        WHERE ti.user_id = "61730143";
        
    '''
    #since we only add data from december 2022 you need to set up in settings at least march 2023 to get all data
    month = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now') AND ti.user_id = "61730143"''', sqliteConnect)
    month1 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-1 months') AND date('now') AND ti.user_id = "61730143"''', sqliteConnect)
    month2 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-2 months') AND date('now', '-1 months') AND ti.user_id = "61730143"''', sqliteConnect)
    month3 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now', '-2 months') AND ti.user_id = "61730143"''', sqliteConnect)
    print(month2)
except sqlite3.IntegrityError as err:
    print(err)








