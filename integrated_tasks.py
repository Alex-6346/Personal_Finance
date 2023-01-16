from splitwise import Splitwise
import sqlite3
from sqlite3 import Error
import json
from sql_queries_methods import create_tables, fill_tables, access_to_splitwise
from sql_currency import currency
from second_task import sql_income
import unrect_transac as unrt 

# unrect_transact = inc-exp+net_debt-fact_balance
# net_debt = (owes_base- owed_base)
# fact balace is the amount to be recorded as income (posite or negative)

# by default fact balance = 0

# if unrect_transact = inc - exp + net_debt - 0 < 0 
# user have more expenses + debt  than  income and owes
# to balance it user can input fact balance as unrect_transact opposite sign

# to visualize current unrecorded transaction amount, by default fact balance = 0
# unrt.unrecorded_transaction_no_write(sObj)

# to retrieve variables used in unrecorded transactions
# give correspondingly 6 variables in given order for each component
# unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(sObj)


# if one wants to visualize an unrecorded transaction for a fact balance of 5000
# input a positive amount to compensate for a negative unrecorded transaction
# input a negative amount to compensate for a positive unrecorded transaction
# unrt.unrecorded_transaction_no_write(sObj, 5000)

# to write in database  fact balance as income use:
# this function will ask user to manually input a fact balance amount
# unrt.unrecorded_transaction_write(sObj)

# be careful when writing onto db as inputs cannot be manually erased
# only can be compensated by inputting same amount in opposite sign to substract


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
    currency(sObj,settings)
        
    
# unrecorded transaction components - without writing user input into database
    #unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrt.unrecorded_transaction_no_write(sObj)
    
    #print(unrecorded_trans, income, expense, net_debt, owes_base, owed_base)
    

# uncomment to store unrecorded transaction with user input fact balance into db
    #unrt.unrecorded_transaction_write(sObj) 



#def run_sync_currency():
#    sObj = access_to_splitwise()
#    splitwise_sync(sObj)
#    currency(sObj,settings)

