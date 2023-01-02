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

def currency(s_obj: Splitwise, settings: dict):

# parsing SQL database to pandas df
    
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
    
# =============================================================================
# extracting start and end dates for currencies request
# =============================================================================
    
    # start date
    dt_strt = str(df_sql['date'].min())
    
    
    # end date, takes maximum date  before or equal to current  date
    dt_end = str(df_sql['date'][df_sql['date'] <=datetime.today().date()].max())
    
    
    
    # =============================================================================
    # list of currencies to request
    # =============================================================================
    
    df_sql.columns
    
    # string of unique currencies, excluding 'EUR'
    curr_str = ','.join(df_sql.currency_code.unique()[df_sql.currency_code.unique() != 'EUR'])
    
    
    
    # =============================================================================
    # requesting url for date range and currencies' list
    #
    # 'EUR' base, exchange rates defined as 'EUR' per foreign currency units
    # =============================================================================
    
    url = f"""https://api.apilayer.com/currency_data/timeframe?source=EUR&currencies={curr_str}&start_date={dt_strt}&end_date={dt_end}"""
    
    payload = {}
    key= {"apikey": settings['fixer_key']}
    
    get_url = requests.get(url, headers=key, data = payload)
    
    json_url = get_url.json()
    
        
    # =============================================================================
    # json to df
    # =============================================================================
    
    # df for exchage rate base EUR with dates as columns
    df_exch = pd.DataFrame(json_url['quotes'])
    
    # EXCHANGE RATE IN DF, EUR AS BASE, ROW DATE 
    # dates as rows and exchage rate as columns base EUR
    df_exch = df_exch.T
    
    
    # removing 'EUR' prefix from column names
    df_exch.columns = df_exch.columns.str.removeprefix('EUR')
    
    
    # index is object 
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
    # filling nan in 'base_amount' columns for base 'EUR'
    # =============================================================================
    
    # where currency is equal to base 'EUR'  base_amount equals amount column
    df_ts.loc[df_ts['currency_code']=='EUR', 'base_amount'] = df_ts['amount']
    
    df_ts.dtypes
    
    
    # =============================================================================
    # exchange rate conversion in EUR :  (currency / base(EUR))
    #
    # FILL 'base_amount' in EUR using for loop,  mask and .loc
    # =============================================================================
    
    # list of currencies except base 'EUR'
    curr_ls = df_ts.currency_code.unique()[df_ts.currency_code.unique() != 'EUR'].tolist()
    
    
    def exch():
        for curr in curr_ls:
        
            mask = df_ts['currency_code'] == curr
                
            df_ts.loc[mask,'base_amount']= df_ts['amount']/df_ts[curr]
                
    exch()
    
    
    # =============================================================================
    # fill sql database with calculated "base_amount" values   --  float type
    # with index columns  "id" (transactions_id) and "user_id"
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









