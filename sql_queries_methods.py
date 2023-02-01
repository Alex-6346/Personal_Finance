import sqlite3

from splitwise import Splitwise
import json
import requests

with open("settings.txt") as f:
    settings = json.load(f)


def access_to_splitwise():
    s_obj = Splitwise(settings['splitwise_name'],
                      settings['splitwise_pass'],
                      api_key=settings['splitwise_key'])
    return s_obj


def create_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Users("
                   "id integer PRIMARY KEY,"
                   "full_name text,"
                   "email text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Groups_users("
                   "id integer PRIMARY KEY,"
                   "group_name text,"
                   "group_type text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Categories("
                   "id integer PRIMARY KEY,"
                   "category_name text type UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Subcategories("
                   "id integer PRIMARY KEY,"
                   "category_id integer,"
                   "subcategory_name text,"
                   "FOREIGN KEY (category_id) REFERENCES Categories(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Transactions("
                   "id integer PRIMARY KEY,"
                   "expense_date datetime,"
                   "group_id integer,"
                   "subcategory_id integer,"
                   "description text,"
                   "currency_code text,"
                   "repeat_interval text,"
                   "updated_date datetime,"
                   "FOREIGN KEY (group_id) REFERENCES Groups_users(id),"
                   "FOREIGN KEY (subcategory_id) REFERENCES Subcategories(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS TransactionItems ("
                   "id integer PRIMARY KEY,"
                   "transaction_id integer,"
                   "user_id integer,"
                   "amount float,"
                   "base_amount float,"
                   "FOREIGN KEY (transaction_id) REFERENCES Transactions(id),"
                   "FOREIGN KEY (user_id) REFERENCES Users(id)"
                   "UNIQUE(transaction_id,user_id))")


def fill_tables(s_obj: Splitwise, cursor):
    user = s_obj.getCurrentUser()
    # Insert information about current user in Users table
    cursor.execute("INSERT OR IGNORE INTO Users (id,full_name,email) VALUES (?,?,?)",
                   [user.getId(), user.getFirstName() + " " + user.getLastName(), user.getEmail()])

    # Get list of friends of a current user, insert information about them in Users table
    other_users = s_obj.getFriends()
    for u in other_users:
        cursor.execute("INSERT OR IGNORE INTO Users (id,full_name,email) VALUES (?,?,?)",
                       [u.getId(), u.getFirstName() + " " + u.getLastName(), u.getEmail()])

    # Insert information about groups in Groups_users table
    groups = s_obj.getGroups()
    for g in groups:
        cursor.execute("INSERT OR IGNORE INTO Groups_users (id,group_name,group_type) VALUES (?,?,?)",
                       [g.getId(), g.getName(), g.getType()])

    # Insert information about categories and subcategories in  Categories and Subcategories tables
    categories = s_obj.getCategories()
    subcategories = []
    for c in categories:
        subcategories.extend(c.getSubcategories())
        cursor.execute("INSERT OR IGNORE INTO Categories (id,category_name) VALUES (?,?)",
                       [c.getId(), c.getName()])
        for s in set(subcategories):
            cursor.execute("INSERT OR IGNORE INTO Subcategories (id,category_id,subcategory_name) VALUES (?,?,?)",
                           [s.getId(), c.getId(), s.getName()])


    # Insert information about expenses and how much every user in it paid in Transactions and TransactionItems tables
    transactions = s_obj.getExpenses()
    for t in transactions:
        cursor.execute("INSERT OR IGNORE INTO Transactions (id,expense_date,group_id,"
                       "subcategory_id,description,currency_code,"
                       "repeat_interval,updated_date) VALUES (?,?,?,?,?,?,?,?)",
                       [t.getId(), t.getDate(), t.getGroupId(), t.getCategory().getId(), t.getDescription(),
                        t.getCurrencyCode(), t.getRepeatInterval(), t.getUpdatedAt()])
        t_users = t.getUsers()
        for t_user in t_users:
            cursor.execute("INSERT OR IGNORE INTO TransactionItems (transaction_id,user_id,amount) VALUES (?,?,?)",
                           [t.getId(), t_user.getId(), t_user.getPaidShare()])

    # Delete expenses for which deleted_date field is not empty from Transactions and TransactionItems tables
    for t in transactions:
        if t.getDeletedAt() is not None:
            cursor.execute('DELETE FROM Transactions WHERE id=(?)', [t.getId()])
            cursor.execute('DELETE FROM TransactionItems WHERE transaction_id=(?)', [t.getId()])

    # Update expenses for which updated_date field is not empty for Transactions and TransactionItems tables
    for t in transactions:
        if t.getUpdatedAt() is not None:
            cursor.execute('UPDATE Transactions SET  expense_date = ? ,group_id = ?,'
                           'subcategory_id = ? ,description = ? ,currency_code = ?,'
                           'repeat_interval = ?, updated_date = ? WHERE id = ?',
                           [t.getDate(), t.getGroupId(), t.getCategory().getId(), t.getDescription(),
                            t.getCurrencyCode(), t.getRepeatInterval(), t.getUpdatedAt(), t.getId()])
            t_users = t.getUsers()
            for t_user in t_users:
                cursor.execute('UPDATE TransactionItems SET  amount = ?  WHERE transaction_id = ? AND user_id = ?',
                               [t_user.getPaidShare(), t.getId(), t_user.getId()])


def insert_category(conn, cursor, category_id: int, category_name: str):
    try:
        cursor.execute("INSERT INTO Categories (id,category_name) VALUES (?,?)",
                   [category_id, category_name])
        conn.commit()
    except sqlite3.IntegrityError as err:
        if str(err) == "UNIQUE constraint failed: Categories.id":
            result = cursor.execute("SELECT * FROM Categories  WHERE id = (?)",
                           [category_id])
            print("Error - a category with id " + str(category_id) + " already exists: " + str(result.fetchone()))
        if str(err) == "UNIQUE constraint failed: Categories.category_name":
            result = cursor.execute("SELECT * FROM Categories  WHERE category_name = (?)",
                                    [category_name])
            print("Error - a category with name " + str(category_name) + " already exists: " + str(result.fetchone()))


def insert_subcategory(conn, cursor, subcategory_id: int, category_id: int, subcategory_name: str):
    try:
        cursor.execute("INSERT INTO Subcategories (id,category_id,subcategory_name) VALUES (?,?,?)",
                       [subcategory_id, category_id, subcategory_name])
        conn.commit()
    except sqlite3.IntegrityError as err:
        if str(err) == "UNIQUE constraint failed: Subcategories.id":
            result = cursor.execute("SELECT * FROM Subcategories  WHERE id = (?)",
                                    [subcategory_id])
            print("Error - a subcategory with id " + str(subcategory_id) + " already exists: " + str(result.fetchone()))
        if str(err) == "UNIQUE constraint failed: Subcategories.subcategory_name":
            result = cursor.execute("SELECT * FROM Subcategories  WHERE subcategory_name = (?)",
                                    [subcategory_name])
            print("Error - a subcategory with name " + str(subcategory_name) + " already exists: " + str(result.fetchone()))
        if str(err) == "FOREIGN KEY constraint failed":
            print("Error - a category with id " + str(category_id) + " does not exist.")



def insert_transaction(conn, cursor, transaction_date: str, group_id: int, subcategory_id: int,
                       description: str, currency_code: str, repeat_interval: str):
    try:
        cursor.execute("INSERT INTO Transactions (expense_date,group_id,subcategory_id,"
                       "description,currency_code,repeat_interval) VALUES (?,?,?,?,?,?)",
                       [transaction_date, group_id, subcategory_id, description,currency_code,repeat_interval])
        conn.commit()
    except sqlite3.IntegrityError as err:
        if str(err) == "FOREIGN KEY constraint failed":
            print("Error - such group id or subcategory id  does not exist.")
        else:
            print(err)

def insert_transaction_item(conn, cursor, transaction_id: int, user_id: int, amount: int):
    try:
        cursor.execute("INSERT INTO TransactionItems (transaction_id, user_id, amount) VALUES (?,?,?)",
                       [transaction_id, user_id, amount])
        conn.commit()
    except sqlite3.IntegrityError as err:
        if str(err) == "FOREIGN KEY constraint failed":
            print("Error - such transaction id or user id  does not exist.")
        else:
            print(err)