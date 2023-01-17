from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt 

print(unrt.__doc__) #for unrecorded transactions function descriptions, arguments and returned values

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
    sql_income(sObj)

    #here insert your new income transaction commands

    currency(sObj,settings)
        

    print(unrt.unrecorded_transaction_no_write(sObj))
    # does not affect db  
    # current unrecorded transaction for default fact balance zero, or pass a second argument number for fact balance
    # unrt.unrecorded_transaction_no_write(sObj, "numeric_value") #replace "numeric_value" by your amount

    #unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(sObj)
    
    
    #unrt.unrecorded_transaction_write(sObj, "numeric_value") # replace "numeric_value" by your amount
    # writes on db fact balance as (positive or negative) income that balance out unrecorded transactions 
    
     



#def run_sync_currency():
#    sObj = access_to_splitwise()
#    splitwise_sync(sObj)
#    currency(sObj,settings)

