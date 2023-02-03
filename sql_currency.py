# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:09:39 2022

@author: calna
"""

import json
import requests
import pandas as pd
import numpy as np
from splitwise import Splitwise
import sqlite3
from datetime import datetime

import json

#%%

def access_to_splitwise():
    with open("settings.txt") as f:
        settings = json.load(f)

    s_obj = Splitwise(settings['splitwise_name'],
                      settings['splitwise_pass'],
                      api_key=settings['splitwise_key'])
    return s_obj

#s_obj = access_to_splitwise()
#%%

# =============================================================================
# Simple sql currency conversion
#
# takes the latest (or saved json-file for) exchange rates 
# =============================================================================

def symbol_date_sqldf():
    
    s_obj = access_to_splitwise()
    
    with sqlite3.connect(str(s_obj.getCurrentUser().getId())+'.sqlite') as conn:
            
        sql_str = """SELECT tr.id,tr.currency_code, trit.user_id, \
trit.amount, trit.base_amount \
FROM Transactions AS tr \
INNER JOIN TransactionItems AS trit \
ON tr.id = trit.transaction_id""" 
    
        df_sql = pd.read_sql(sql_str, conn)
                
    # # string of unique currencies, excluding 'EUR'
    # curr_str = ','.join(df_sql.currency_code.unique()[
    #     df_sql.currency_code.unique() != 'EUR'])
    
    return df_sql



#%%

def fixer_api_latest():
    '''
    request all latest currency rates only once a day and saves them to json file
    '''
    
    settings = pd.read_json('settings.txt', typ='series')
    
    url = """https://api.apilayer.com/currency_data/live?source=EUR"""
    
    payload = {}
    key= {"apikey": settings['fixer_key2']}
    
    # connect to api and verify status code before pulling data
    get_url = requests.get(url, headers=key, data = payload)
    status_code = get_url.status_code
    

    if status_code == 200 and settings['current_date'] != str(datetime.now().date()):
        
        settings['current_date'] = str(datetime.now().date())
        
        settings.to_json('settings.txt')
        
        with open ('exchange_rate.json','w') as f:
            json.dump(get_url.json(), f)
    
    elif status_code == 200 and settings['current_date'] == str(datetime.now().date()):
        status_code = None
    
    # if no status_code error updates only once a day currency rates in file                
    return status_code

#%%

# =============================================================================
# calculates exchange rates in base EUR:  (foreign symbols / base(EUR))
# and fills "base_amount" column in SQL database
# =============================================================================

def currency():
    
    s_obj = access_to_splitwise()
    
    df_sql = symbol_date_sqldf()
    
    #json_url, status = fixer_api(date_start, date_end, symbols, settings)
    
    status = fixer_api_latest()
    
    # reading exchange rate from json local file
    with open ('exchange_rate.json','r') as f:
        json_exch= json.load(f)       # load for reading json file f

    
        
    # df for exchage rate base EUR with dates as columns
    # EXCHANGE RATE IN Rows, DATE in Columns
    df_exch = pd.DataFrame(json_exch['quotes'], index=[0])
    
    # remove 'EUR' prefix from column names
    #df_exch.columns = df_exch.columns.str.removeprefix('EUR')
    new_ex = []
    for ex in df_exch.columns:
        new_ex.append(ex[3:])

    # currencies without 'EUR' names
    df_exch.columns = new_ex
    
    # dates as rows and exchage rate as columns base EUR
    df_exch = df_exch.T
    
    # renaming column
    df_exch.columns = ['exch_base_EUR']


    df_sql.columns    
    # =============================================================================
    # joining df_exch and df_sql
    # =============================================================================
    df_ts = df_sql.join(df_exch, on='currency_code', how='left')
    
    # dropping old dfs
    del df_sql
    del df_exch
    
    # setting column to float type
    #df_ts['base_amount'] = df_ts['base_amount'].astype('float')
    
    
    # =============================================================================
    # fill df nan in 'base_amount' columns for base 'EUR' symbol
    # =============================================================================
    
    # where currency is equal to base 'EUR'  base_amount equals amount column
    df_ts.loc[df_ts['currency_code']=='EUR', 'base_amount'] = df_ts['amount']
    
    
    df_ts.dtypes
        
    # list of currencies except base 'EUR'
    curr_ls = df_ts.currency_code.unique()[
        df_ts.currency_code.unique() != 'EUR'].tolist()
    
    # =============================================================================
    # FILL df 'base_amount' in EUR  with for loop, index-mask and .loc in "exch()"
    #
    # exchange rate conversion in EUR :  (foreign currency symbols / base(EUR))
    # =============================================================================
    for curr in curr_ls:
        
        mask = df_ts['currency_code'] == curr
                
        df_ts.loc[mask,'base_amount']= df_ts['amount']/df_ts['exch_base_EUR']
          
    
    
    # =============================================================================
    # fill SQL database "base_amount" values   --  float type
    # based on index columns  "id" (transactions_id) and "user_id"
    # =============================================================================
    
    with sqlite3.connect(str(s_obj.getCurrentUser().getId())+'.sqlite', timeout=10) as conn:
        
        # Insert df into MySQL
        df_ts[['id','user_id','base_amount']].to_sql(
            'Exch', con = conn, if_exists = 'replace')
        
        sql_str = """UPDATE TransactionItems AS trit \
    SET base_amount = ex.base_amount \
    FROM Exch AS ex \
    WHERE trit.transaction_id = ex.id and trit.user_id = ex.user_id"""
        
        cur = conn.cursor()
        
        cur.execute(sql_str)
        
        conn.commit()
        
        sql_str = """DROP TABLE Exch"""
    
        cur.execute(sql_str)
        
        conn.commit()
    
    return status


#%%



