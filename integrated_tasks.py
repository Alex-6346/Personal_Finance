from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt 

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
    status = currency()
    print(f'\nAPI status code: {status} \n"200" success. Today´s rates saved to file\n\
Other than "200" an API error ocurred. Old rates taken from local file\n\
"None", not necessary a new call. Today´s rates taken from local file\n')
    
    unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(0)

    print(f"\nAll reported amounts are in Euros (€)\n\nunrecorded transactions:{unrecorded_trans},\n\
    total income: {income},\ntotal expenses: {expense},\nnet debt: {net_debt},\n\
    total owes: {owes_base},\ntotal owed: {owed_base}")



if __name__ == '__main__':

    sObj = access_to_splitwise()
    splitwise_sync(sObj)
    sql_income(sObj)
    
    status = currency()
      
    # Does not write on database
    # change 0 for othe number that u want for fact balance
    unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(0)
    
    unrt.unrecorded_transaction_no_write()
    
    unrt.unrecorded_transaction_no_write(13020)
    
    print(f"\nAll reported amounts are in Euros (€)\n\nunrecorded transactions:{unrecorded_trans},\n\
total income: {income},\ntotal expenses: {expense},\nnet debt: {net_debt},\n\
total owes: {owes_base},\ntotal owed: {owed_base}")
    
    
    # Writes on database only  when fact balance is different than zero
    # writes on db fact balance as (positive or negative) income that balance out unrecorded transactions 
    unrt.unrecorded_transaction_write(0) # replace 0 by your fact balance
    

    