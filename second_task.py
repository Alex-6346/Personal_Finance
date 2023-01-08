import sqlite3
from datetime import datetime
from sqlite3 import Error
from splitwise import Splitwise
from dateutil import parser


from sql_queries_methods import insert_category, insert_transaction, insert_subcategory, insert_transaction_item, \
    access_to_splitwise

if __name__ == '__main__':
    s_obj = access_to_splitwise()
    user = s_obj.getCurrentUser()
    user_id = user.getId()
    try:
        conn = sqlite3.connect(str(user_id) + ".sqlite")
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
    except Error as e:
        print(e)

    insert_category(conn, cursor, 100, 'Income')
    insert_subcategory(conn, cursor, 101, 100, 'Salary')
    insert_subcategory(conn, cursor, 102, 100, 'Business')
    insert_subcategory(conn, cursor, 103, 100, 'Gifts')
    insert_subcategory(conn, cursor, 104, 100, 'Grants')
    insert_subcategory(conn, cursor, 105, 100, 'Other')

    #Example of entering the date
    #date_entry = input('Enter a date in YYYY-MM-DD format')
    #year, month, day = map(int, date_entry.split('-'))
    #time_entry = input('Enter a time in HH:MM:SS format')
    #hour, minute, second = map(int, time_entry.split(':'))
    #date = datetime(year, month, day, hour, minute, second).strftime('%Y-%m-%dT%H:%M:%SZ')

    insert_transaction(conn, cursor, '2022-12-20T15:46:56Z', 41498693, 101, 'testSalary', 'USD', None)
    transaction_id = cursor.lastrowid
    insert_transaction_item(conn, cursor, transaction_id, 61730143, 20.5)
    insert_transaction_item(conn, cursor, transaction_id, 61730735, 24.5)
