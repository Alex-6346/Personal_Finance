import sqlite3
import pandas as pd
import matplotlib

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
        WHERE ti.user_id = "61730143" AND ;
        
    '''
    #since we only add data from december 2022 you need to set up in settings at least march 2023 to get all data
    month = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now') AND ti.user_id = "61730143"''', sqliteConnect)
    month1 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-1 months') AND date('now') AND ti.user_id = "61730143"''', sqliteConnect)
    month2 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-2 months') AND date('now', '-1 months') AND ti.user_id = "61730143"''', sqliteConnect)
    month3 = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now', '-2 months') AND ti.user_id = "61730143"''', sqliteConnect)
    repeat = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE repeat_interval = "monthly" AND ti.user_id = "61730143"''', sqliteConnect)
    expenses = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE category_id NOT LIKE '100' AND ti.user_id = "61730143"''', sqliteConnect)
    income = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE category_id LIKE '100' AND ti.user_id = "61730143"''', sqliteConnect)
    print(income)
except sqlite3.IntegrityError as err:
    print(err)


#need to get rid off salary
#need to seperate expenses with repeat interval





