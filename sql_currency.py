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

#%%

# Parses Splitwise SQL database to df
# Retrieves transactions currency symbols and dates

def symbol_date_sqldf(s_obj: Splitwise):

    with sqlite3.connect(str(s_obj.getCurrentUser().getId())+'.sqlite') as conn:
            
        sql_str = """SELECT tr.id,tr.expense_date,tr.currency_code, trit.user_id, \
trit.amount, trit.base_amount \
FROM Transactions AS tr \
INNER JOIN TransactionItems AS trit \
ON tr.id = trit.transaction_id""" 
    
        df_sql = pd.read_sql(sql_str, conn)
            
        
    # parsing dates in default 'UCT'
    # starts on 30 Nov 23Hr  instead of 1 Dec 00Hr   
    # =============================================================================
    #  parsing expense_date column to 'CET' datetime zone
    # =============================================================================
    df_sql['expense_date'] = pd.to_datetime(df_sql['expense_date']).dt.tz_convert('CET')
            
    # =============================================================================
    # 'date' column  without time
    # =============================================================================
    df_sql['date'] = df_sql['expense_date'].dt.date
        
    
    # start date
    dt_strt = str(df_sql['date'].min())
    
# =============================================================================
#   # end date, takes maximum date  before or equal to current  date
# =============================================================================
    dt_end = str(df_sql['date'][df_sql['date'] <=datetime.today().date()].max())
    
    # string of unique currencies, excluding 'EUR'
    curr_str = ','.join(df_sql.currency_code.unique()[df_sql.currency_code.unique() != 'EUR'])
    
    return dt_strt, dt_end, curr_str, df_sql


#%%

# =============================================================================
# Connects to fixes.io API with key in setting.txt
#
# Requests date range (between start and end date) and currency symbols 
# obtained from  symbol_date_sqldf() function
#
# 'EUR' base, exchange rates defined as 'EUR' per foreign currency units
# =============================================================================

def fixer_api(date_start, date_end, symbols, settings):
    
    url = f"""https://api.apilayer.com/currency_data/timeframe?source=EUR&currencies={symbols}&start_date={date_start}&end_date={date_end}"""
    
    payload = {}
    key= {"apikey": settings['fixer_key']}
    
    get_url = requests.get(url, headers=key, data = payload)
    
    return get_url.json()
    


#%%

# =============================================================================
# calculates exchange rates in base EUR:  (foreign symbols / base(EUR))
# and fills "base_amount" column in SQL database
# =============================================================================

def currency(s_obj: Splitwise, settings: dict):
    
    date_start, date_end, symbols, df_sql = symbol_date_sqldf(s_obj)
    
    json_url = fixer_api(date_start, date_end, symbols, settings)
    
        
    # df for exchage rate base EUR with dates as columns
    # EXCHANGE RATE IN Rows, DATE in Columns
    df_exch = pd.DataFrame(json_url['quotes'])
    
    # dates as rows and exchage rate as columns base EUR
    df_exch = df_exch.T
    
    # remove 'EUR' prefix from column names
    #df_exch.columns = df_exch.columns.str.removeprefix('EUR')
    new_ex = []
    for ex in df_exch.columns:
        new_ex.append(ex[3:])

    df_exch.columns = new_ex


    # row index is 'object', not datetime type
    df_exch.index.dtype
    
    # setting index as datetime
    df_exch.index = pd.to_datetime(df_exch.index)
    
        
    # =============================================================================
    # joining df_exch and df_sql
    # =============================================================================
    df_ts = df_sql.set_index('date').join(df_exch).reset_index()
    
    # dropping old dfs
    del df_sql
    del df_exch
    
    # setting column to float type
    df_ts['base_amount'] = df_ts['base_amount'].astype('float')
    
    
    # =============================================================================
    # fill df nan in 'base_amount' columns for base 'EUR' symbol
    # =============================================================================
    
    # where currency is equal to base 'EUR'  base_amount equals amount column
    df_ts.loc[df_ts['currency_code']=='EUR', 'base_amount'] = df_ts['amount']
    
    df_ts.dtypes
        
    # list of currencies except base 'EUR'
    curr_ls = df_ts.currency_code.unique()[df_ts.currency_code.unique() != 'EUR'].tolist()
    
    # =============================================================================
    # FILL df 'base_amount' in EUR  with for loop, index-mask and .loc in "exch()"
    #
    # exchange rate conversion in EUR :  (foreign currency symbols / base(EUR))
    # =============================================================================
    for curr in curr_ls:
        
        mask = df_ts['currency_code'] == curr
                
        df_ts.loc[mask,'base_amount']= df_ts['amount']/df_ts[curr]
          
    
    
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


#%%



