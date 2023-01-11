from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json

from sql_queries_methods import create_tables, fill_tables, access_to_splitwise

from sql_currency import currency

with open("settings.txt") as f:
    settings = json.load(f)

def splitwise_sync(s_obj: Splitwise):
    user = s_obj.getCurrentUser()
    user_id = user.getId()
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(str(user_id) + ".sqlite")
        cursor = conn.cursor()
    except Error as e:
        print(e)

    # TODO: Exception handling
    create_tables(cursor)
    fill_tables(s_obj, cursor)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    sObj = access_to_splitwise()
    splitwise_sync(sObj)
    currency(sObj,settings)

def run_sync_currency():
    sObj = access_to_splitwise()
    splitwise_sync(sObj)
    currency(sObj,settings)