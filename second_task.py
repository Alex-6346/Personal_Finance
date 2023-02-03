import sqlite3
from datetime import datetime
import random as rand
#from random import randint, random
from sqlite3 import Error
from splitwise import Splitwise
from dateutil import parser


from sql_queries_methods import insert_category, insert_transaction, insert_subcategory, insert_transaction_item, \
    access_to_splitwise
 
    
def sql_income(s_obj: Splitwise):    
    
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

"""
    insert_transaction(conn, cursor, '2022-12-20T15:46:56Z', 41498693, 101, 'Salary', 'USD', "monthly")
    transaction_id_salary = cursor.lastrowid
    insert_transaction(conn, cursor, '2022-12-20T15:46:56Z', 41498693, 102, 'Business', 'USD', None)
    transaction_id_business = cursor.lastrowid
    insert_transaction(conn, cursor, '2022-12-20T15:46:56Z', 41498693, 103, 'Gifts', 'USD', None)
    transaction_id_gifts = cursor.lastrowid
    insert_transaction_item(conn, cursor, transaction_id_salary, 61730143, 3600)
    insert_transaction_item(conn, cursor, transaction_id_salary, 61730735, 4200)
    insert_transaction_item(conn, cursor, transaction_id_salary, 61730736, 3600)
    insert_transaction_item(conn, cursor, transaction_id_gifts, 61730143, 30)
    insert_transaction_item(conn, cursor, transaction_id_business, 61730143, 700)

    # Creating 20 random Income transactions for Max Mustermann

    for x in range(20):
        subcategory_id = rand.randint(101, 105)
        amount = rand.randint(1, 100)

        year = str(rand.randint(2021, 2023))
        month = str(rand.randint(1, 12))
        day = str(rand.randint(1, 28))
        insert_transaction(conn, cursor, '2022-12-20T15:46:56Z', None, subcategory_id, str(x) + 'test income', 'EUR',
                           None)
        transaction_id = cursor.lastrowid
        insert_transaction_item(conn, cursor, transaction_id, 61730143, amount)
"""
