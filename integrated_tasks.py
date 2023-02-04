from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt 
from random_loop import loop_control

#See unrecorded transactions function descriptions, arguments and returned values
#print(unrt.__doc__) 

# def settings():
#     with open("settings.txt") as f:
#         settin = json.load(f)
#     return settin


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

##First Task##
def run_sync():
    
    sObj = access_to_splitwise()
    splitwise_sync(sObj)
    sql_income(sObj)
    loop_control() # loop_control(20,40)  [(income, expenses)]
    currency()
    unrt.unrecorded_transaction_no_write()
    #unrt.unrecorded_transaction_write()

#%%

if __name__ == '__main__':

    run_sync()
    