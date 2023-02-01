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

    #pie charts of expenses per subcategory for the last 3 months (one chart per month)
    #since we only add data from december 2022 you need to set up in settings at least march 2023 to get all data
    month = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now') AND ti.user_id = "61730143" AND category_id NOT LIKE "100"''', sqliteConnect)
    month1_exp = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-1 months') AND date('now') AND ti.user_id = "61730143" AND category_id NOT LIKE "100"''', sqliteConnect)
    month2_exp = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-2 months') AND date('now', '-1 months') AND ti.user_id = "61730143" AND category_id NOT LIKE "100"''', sqliteConnect)
    month3_exp = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now', '-2 months') AND ti.user_id = "61730143" AND category_id NOT LIKE "100"''', sqliteConnect)
    repeat = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE repeat_interval = "monthly" AND ti.user_id = "61730143"''', sqliteConnect)

except sqlite3.IntegrityError as err:
    print(err)


#need to get rid off salary
#need to seperate expenses with repeat interval


income = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE category_id LIKE '100' AND ti.user_id = "61730143"''', sqliteConnect)
    


