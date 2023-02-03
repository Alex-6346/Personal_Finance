from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise, insert_transaction, \
    insert_transaction_item
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt 

#See unrecorded transactions function descriptions, arguments and returned values
#print(unrt.__doc__) 

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
    
    # run currency(sObj,settings), only after u insert all ur income rows
    currency(sObj,settings)
    
    
    # Does not write on database
    # change 0 for othe number that u want for fact balance
    unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(sObj,0)


    print(f"\nAll reported amounts are in Euros (€)\n\nunrecorded transactions:{unrecorded_trans},\n\
total income: {income},\ntotal expenses: {expense},\nnet debt: {net_debt},\n\
total owes: {owes_base},\ntotal owed: {owed_base}")

    unrt.unrecorded_transaction_no_write(sObj, -33740)


    # Writes on database only  when fact balance is different than zero
    # writes on db fact balance as (positive or negative) income that balance out unrecorded transactions 
    unrt.unrecorded_transaction_write(sObj, 0) # replace 0 by your fact balance

    unrt.unrecorded_transaction_write(sObj, -46294)

##First Task##
def run_sync():
    sObj = access_to_splitwise()
    splitwise_sync(sObj)