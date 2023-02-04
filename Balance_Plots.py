# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:59:34 2023

@author: calna
"""

# Prediction
#from sklearn import linear_model
#import numpy as np
import pandas as pd
import sqlite3
#from datetime import datetime
import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly as py

#from sql_queries_methods import insert_transaction, insert_transaction_item

from splitwise import Splitwise
import json
#import requests

#%%

def access_to_splitwise():
    with open("settings.txt") as f:
        settings = json.load(f)

    s_obj = Splitwise(settings['splitwise_name'],
                      settings['splitwise_pass'],
                      api_key=settings['splitwise_key'])
    return s_obj

#%%

def reg_income_expenses(method="Income", category='100'):
    
    s_obj = access_to_splitwise()
    
    if method.lower() == "income":
        sign = '='
    else:
        sign = "!="
    
    #s_obj = '61730143'
    with sqlite3.connect(str(s_obj.getCurrentUser().getId())+'.sqlite') as conn:
            
        sql_str = f"""SELECT trans.expense_date, sub.id, sub.category_id,\
        trans.subcategory_id, \
        trans.id, item.transaction_id, item.base_amount \
        FROM Subcategories AS sub \
        INNER JOIN Transactions AS trans ON trans.subcategory_id = sub.id \
        INNER JOIN TransactionItems AS item ON item.transaction_id = trans.id \
        WHERE sub.category_id {sign} {category} """ 
    
        df_sql = pd.read_sql(
            sql_str, conn, parse_dates='expense_date')
        
        df_sql = df_sql.drop(['id','id','transaction_id'], axis=1)
        
        #df_sql = df_sql.drop(['id','id'], axis=1)
        
        df_sql = df_sql.rename(columns={'expense_date':'date'})
        
        #df_sql = df_sql.set_index('date')
        
        # removing transactions with zero entries
        df_sql = df_sql[df_sql['base_amount']!=0].sort_values(by='date')
        
        # Calculating daily sums  and cummulative sums over days
        
        #groupby('Date').Amount.sum()
        
    return df_sql

#%%

def daily_inc_exp(method='income'):

    df = reg_income_expenses(method)
       
    # test
    #df = df_inc.copy()
    
    df_daily = df.groupby(['date'])['base_amount'].sum().reset_index()
    
    df_daily.columns
    
    df_daily = df_daily.rename(columns={'base_amount':'dly_amount'})
    
    df_daily['cumm_dly_amount'] = df_daily['dly_amount'].cumsum()
    
    df_daily = df_daily.set_index('date')
    
    return df_daily

#%%

def daily_balances():
    
    dly_exp = daily_inc_exp('expenses')
    
    dly_inc = daily_inc_exp()
    
    #dly_exp = df_dly_exp.copy()
    #dly_inc = df_dly_inc.copy() 
    
    dly_bal = dly_inc.join(dly_exp, how='outer',
                           lsuffix='_inc', rsuffix='_exp').fillna(0)
    
    dly_bal.columns
    
    dly_bal['dly_amount'] = dly_bal['dly_amount_inc'] - dly_bal['dly_amount_exp']
    
    dly_bal['cumm_dly_amount'] = dly_bal['dly_amount'].cumsum()
    
    dly_bal['cumm_dly_amount_inc'] = dly_bal['dly_amount_inc'].cumsum()
    
    dly_bal['cumm_dly_amount_exp'] = dly_bal['dly_amount_exp'].cumsum()
    
    return dly_bal
    


#%%


def plot_bal_cummsum():

    df = daily_balances()
    
    plot_ls = []
    
    fig = {}
    
    #ax = {}
    
    name = ['income','expenses','balances']
    
    for i in range(int(len(df.columns)/2)):
        
        fig[i], ax = plt.subplots(2,1, figsize=(8,6), sharex=True)
        
        df.iloc[:,i*2].plot(marker='o', ax=ax[0])
        
        ax[0].set_title(f'daily {name[i]}')
        
        ax[0].grid()
        
        df.iloc[:,1+i*2].plot(ax=ax[1], color='m')
        
        ax[1].set_title(f'cummulative daily {name[i]}')
        
        ax[1].grid()
        
        #fig[i].supylabel("euros €")
        
        # hspace vertical space, wspace horizontal
        fig[i].subplots_adjust(hspace=0.3)
        
        fig[i].savefig(f'daily_{name[i]}.jpg', format='jpg')
        
        plot_ls.append(fig[i])
    
    return plot_ls

#%%

if __name__ == "__main__":

    plots_ls = plot_bal_cummsum()

    plots_ls[0]
    
    plots_ls[1]
    
    plots_ls[2]

    def download_balance():
        plots_ls[2].savefig("daily_balances.pdf", format = 'pdf')

