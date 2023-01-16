# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:43:32 2023

@author: calna
"""

#%%

# READ ME

# DATA Content and output

# all amounts are reported in "EUR" currency by default

# it calculates Splitwise User total sum for income, expenses, user owes, user owed
# net debt (user owes - user owed )
# fact balance requires user value input

# following this definition
# unrecorded transactions = (incomes - expenses + net debt - fact balance)*(-1)

# user owes, user owed  foreign currency transactions are converted to "EUR"
# at the latest exchange rates 

#%%

# FUNCTIONABILITY

# unrecorded_transaction_no_write(s_obj: Splitwise, zero_fact_balance = 0.0)

# reports income, expeses, net debt, user owes, user owed and unrecorded transactions
#  for user Fact balance default to zero
#                        without writing unrecorded transaction to the database


# required arguments: s_obj -splitwise user credentials- and fact_balance (float - set by default to zero)

# example for retrieving variables
# unrecorded_trans, income, expense, net_debt, owes_base, owed_base = unrecorded_transaction_no_write(s_obj)


#############################################################################

# unrecorded_transaction_write(s_obj)

# after running it asks user to input his fact balance

# ***  modifies permanently the database  ***

# it only writes into database the amount calculated for unrecorded transactions
# given fact balance input manually by user



#%%

import pandas as pd
#import numpy as np
import sqlite3
from datetime import datetime

from sql_queries_methods import insert_transaction, insert_transaction_item

from splitwise import Splitwise
#from splitwise.expense import Expense
import json
import requests

#%%

with open("settings.txt") as f:
    settings = json.load(f)


def access_to_splitwise():
    s_obj = Splitwise(settings['splitwise_name'],
                      settings['splitwise_pass'],
                      api_key=settings['splitwise_key'])
    return s_obj

s_obj = access_to_splitwise()

#%%

def income_expenses(s_obj: Splitwise, method="Income", category='100'):
    
    if method.lower() == "income":
        sign = '='
    else:
        sign = "!="
    
    #s_obj = '61730143'
    with sqlite3.connect(str(s_obj.getCurrentUser().getId())+'.sqlite') as conn:
            
        sql_str = f"""SELECT sub.id, sub.category_id, trans.subcategory_id, \
        trans.id, item.transaction_id, item.base_amount \
        FROM Subcategories AS sub \
        INNER JOIN Transactions AS trans ON trans.subcategory_id = sub.id \
        INNER JOIN TransactionItems AS item ON item.transaction_id = trans.id \
        WHERE sub.category_id {sign} {category} """ 
    
        df_sql = pd.read_sql(sql_str, conn)
        
        sum = df_sql['base_amount'].sum()
        
    return sum


#%%
#exp = income_expenses(s_obj, 'ExpeNditure')

#inc = income_expenses(s_obj)

#%%

def friends_balance_currency(s_obj: Splitwise):    
    
    # calls Splitwise User's each Friend balance in different currencies
    friends = s_obj.getFriends()
    
    f_ls = []
    
    for f in friends:
        bals = f.balances
        f_ls.append(bals)
    
    amount = [[],[]]
    for i in f_ls:
        for j in i:
            amount[1].append(float(j.amount))
            amount[0].append(j.currency_code)
            

    bal_df = pd.DataFrame(amount).T
    
    bal_df.columns = ['symbol','amount']
    
    # net debt as owes + owed
    #net_debt_curr = bal_df.groupby('symbol').sum()
    
    
    # split df between User owns and owned 
    # then group by currency and add amounts in same currency for each df
    
    owes = bal_df[bal_df['amount']<0].groupby('symbol').sum()
    
    owes.columns = ['owes'] # renaming column
    
    owed = bal_df[bal_df['amount']>0].groupby('symbol').sum()
    
    owed.columns = ['owed'] # renaming column
    
    # join owes and owned into on df and fill nan with 0
    balance_curr = owes.join(owed, how='outer').fillna(0)
    
    curr_str = ','.join(bal_df['symbol'].unique())
    
    return curr_str, balance_curr
                

symbols, balance_curr = friends_balance_currency(s_obj)

#%%

#def fixer_api_latest(symbols, settings):
    
#    url = f"""https://api.apilayer.com/currency_data/live?source=EUR&currencies={symbols}"""
    
#    payload = {}
#    key= {"apikey": settings['fixer_key2']}
    
#    get_url = requests.get(url, headers=key, data = payload)
    
#    with open ('exchange_rate.json','w') as f:
#        json.dump(get_url.json(), f)
    
#    return get_url.json()

#%%
'''
def fixer_api_latest(settings):
    
    settings = pd.read_json('settings.txt', typ='series')
    
    # old function now deprecated and broken
    #url = f"""https://api.apilayer.com/currency_data/live?source=EUR&currencies={symbols}"""
    
    url_1 = """https://api.apilayer.com/currency_data/live?source=EUR"""
    
    url_2 = """https://api.apilayer.com/fixer/latest?source=EUR"""
    
    payload = {}
    key= {"apikey": settings['fixer_key2']}
    
    # request all latest currency rates only once a day and saves them to file
    
    if settings['current_date'] != str(datetime.now().date()):
        
        settings['current_date'] = str(datetime.now().date())
        
        settings.to_json('settings.txt')
        
        if (datetime.now().weekday() // 2) != 0:
            
            url = url_1
            
            get_url = requests.get(url, headers=key, data = payload)
            
            with open ('exchange_rate.json','w') as f:
                json.dump(get_url.json(), f)
            
        else:
            url = url_2
            
            get_url = requests.get(url, headers=key, data = payload)
            
            with open ('exchange_rate.json','w') as f:
                json.dump(get_url.json(), f)
        
'''
#%%

def fixer_api_latest(settings):
    '''
    # request all latest currency rates only once a day and saves them to json file
    '''
    
    settings = pd.read_json('settings.txt', typ='series')
    
    url = """https://api.apilayer.com/currency_data/live?source=EUR"""
    
    payload = {}
    key= {"apikey": settings['fixer_key2']}
    
    if settings['current_date'] != str(datetime.now().date()):
        
        settings['current_date'] = str(datetime.now().date())
        
        settings.to_json('settings.txt')
            
        get_url = requests.get(url, headers=key, data = payload)
        
        with open ('exchange_rate.json','w') as f:
            json.dump(get_url.json(), f)


#%%

def friends_balance_euros(s_obj: Splitwise, settings: dict):
    
    symbols, balance_curr = friends_balance_currency(s_obj)
    
    #json_url = fixer_api_latest(symbols, settings)
    fixer_api_latest(settings)
    
    # reading exchange rate from json local file
    with open ('exchange_rate.json','r') as f:
        exch_rates = json.load(f)       # load for reading json file f
    
        
    # df for exchage rate base EUR with dates as columns
    # EXCHANGE RATE IN Rows, DATE in Columns
    #df_exch = pd.DataFrame(json_url['quotes'], index=[0])
    
    df_exch = pd.DataFrame(exch_rates['quotes'], index=[0])
    
    
    df_exch.columns

    # remove 'EUR' prefix from column names
    #df_exch.columns = df_exch.columns.str.removeprefix('EUR')
    new_ex = []
    for ex in df_exch.columns:
        new_ex.append(ex[3:])
        
    # assigning new column names
    df_exch.columns = new_ex
    
    # transposing matrix to make currencies appear in rows
    df_exch = df_exch.T
    
    # renaming column
    df_exch.columns = ['quote']
    
    # both df should have same index type
    df_exch.index
    balance_curr.index
    
    # =============================================================================
    # joining df_exch and df_sql, 
    #     in df_exch 'EUR' is not reported as it the base of the currency rates
    # =============================================================================
    df_ts = balance_curr.join(df_exch, how='outer')
    
    df_ts.index
    
    df_ts.dtypes
    
    df_ts.columns
    
    # fill with 1, the quote, or exchange rate for 'EUR' as 'EUR' is the base
    df_ts.at['EUR', 'quote'] = 1
    
    # dropping old dfs
    #del df_net_debt_curr
    #del df_exch
    
    # setting column to float type
    #df_ts['base_amount'] = df_ts['base_amount'].astype('float')
    
    # owes and owed in EUR base
    df_ts['owes_base'] = df_ts['owes']/df_ts['quote']
    
    df_ts['owed_base'] = df_ts['owed']/df_ts['quote']
    
    # total User owes in EUR base
    owes_base = abs(df_ts['owes_base'].sum())
    
    # total User owes in EUR base
    owed_base = df_ts['owed_base'].sum()
    
    # net debt owes_base + owed_base
    net_debt = owes_base - owed_base
    
    return owes_base, owed_base, net_debt

#%%

def insert_transaction_item_base(conn, cursor, transaction_id: int, user_id: int, amount: int):
    try:
        cursor.execute("INSERT INTO TransactionItems (transaction_id, user_id, amount, base_amount) VALUES (?,?,?,?)",
                       [transaction_id, user_id, amount, amount])
        conn.commit()
    except sqlite3.IntegrityError as err:
        if str(err) == "FOREIGN KEY constraint failed":
            print("Error - such transaction id or user id  does not exist.")
        else:
            print(err)

#%%

def unrecorded_transaction_no_write(s_obj: Splitwise, fact_balance = 0.0):
    
    exp = income_expenses(s_obj, 'ExpeNditure')

    inc = income_expenses(s_obj)
    
    owes_base, owed_base, net_debt = friends_balance_euros(s_obj, settings)
    
    # unrecorded transactions for zero fact balance input by user
    # with negative sign, just as in PersonalFinance.pdf
    unrec_trans_zero_factbal = inc - exp + net_debt - (-fact_balance)
    
    return unrec_trans_zero_factbal, inc, exp, net_debt, owes_base, owed_base


#%%


def unrecorded_transaction_write(s_obj: Splitwise):
    
    while True:
        
        try: 
            fact_balance = float(input('Please enter your fact balance amount: '))
            break
        
        except ValueError:
            print("\nPlease enter a numeric amount \n")
            continue
    
    unrecord_trans, inc, exp, net_debt, owes_base, owed_base = unrecorded_transaction_no_write(s_obj, fact_balance)
    
    if fact_balance != 0:
    
        user_id = s_obj.getCurrentUser().getId()
        

        # UTC datetime zone format report by Splitwise
        # 2023-01-05T23:00:00Z 
        todays_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                
        group_id = None
        
        subcategory = 105
        
        description = "Unrecorded Transactions"
        
        currency = 'EUR'
        
        repeat_interval = None
        
            
        with sqlite3.connect(str(user_id)+'.sqlite') as conn:
            
            cursor = conn.cursor()
        
            insert_transaction(conn, cursor, todays_date, group_id, subcategory, 
                               description,currency, repeat_interval)
                
            transaction_id = cursor.lastrowid
             
            # inserts unrecorded_transaction for fact_balance set by user
            insert_transaction_item_base(conn, cursor, transaction_id, user_id, fact_balance)
            
            conn.commit()
            
            #conn.close()
        
        #return unrecorded_transaction_no_write(s_obj, fact_balance)
        return unrecorded_transaction_no_write(s_obj)
    
    else:
        
        return unrecorded_transaction_no_write(s_obj)


#%%
'''
unrecord_trans, inc, exp, net_debt  =  unrecorded_transaction_no_write(s_obj)

print(f'inc = {inc}\nexp = {exp}\nnet_debt = {net_debt}\nunrecorded transactions = inc - exp + net debt \nunrecorded transactions = {unrecord_trans}')

#%%

unr_test = unrecorded_transaction_write(s_obj)

print(unr_test)
'''

#%%

#unrec_trans_zero_factbal, inc, exp, net_debt, owes_base, owed_base =  unrecorded_transaction_no_write(s_obj)

#print(unrec_trans_zero_factbal, inc, exp, net_debt, owes_base, owed_base)

#%%









