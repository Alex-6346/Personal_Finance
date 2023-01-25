import sqlite3
import pandas as pd

try:
    sqliteConnection = sqlite3.connect("61730143.sqlite")
    cursor = sqliteConnection.cursor()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


try:
    start_date = "2023-02-01" #from this date on it will take the last 3 months
    query = """
        SELECT * FROM Transactions AS t
        INNER JOIN TransactionItems AS ti
            ON t.id = ti.transaction_id
        INNER JOIN Subcategories as s
            ON s.id = t.subcategory_id
        WHERE t.expense_date > "2022-12-01";
    """
    result = pd.read_sql(sql = query, con = sqliteConnection)
    result.to_csv("test.csv")
    print(result)
except sqlite3.IntegrityError as err:
    print(err)








