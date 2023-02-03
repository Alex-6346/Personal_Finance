# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:59:34 2023

@author: calna
"""

# Prediction
from sklearn import linear_model
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py

from sql_queries_methods import insert_transaction, insert_transaction_item

from splitwise import Splitwise
import json
import requests

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
    
    return dly_bal
    


#%%
'''
def daily_inc_exp(s_obj,method='income'):

    df_daily = reg_income_expenses(s_obj, method)
       
    df_daily['dly_amount'] = df_daily.groupby(df_daily.sort_index().index)[
        'base_amount'].sum()
    
    df_daily['cumm_dly_amount'] = df_daily['dly_amount'].cumsum()
    
    return df_daily
'''

#%%

s_obj = access_to_splitwise()

df_inc = reg_income_expenses()

df_inc.columns

df_exp = reg_income_expenses( 'expense')

#%%

# TOTAL INCOME SUM
df_inc.base_amount.sum()

# TOTAL EXPENSE SUM
df_exp.base_amount.sum()

#%%

df_dly_inc = daily_inc_exp()

df_dly_exp = daily_inc_exp('expense')


df_exp.columns

df_inc.dtypes

#%%

# =============================================================================
# ploting daily sums and cummulative sums over period
# =============================================================================

# ploting dly exp

fig_dly_exp, ax_dly_exp = plt.subplots()

df_dly_exp['dly_amount'].plot(marker='o', ax=ax_dly_exp)

ax_dly_exp.set_title('user daily expenses')

#%%

# ploting cumm dly exp

fig_cdly_exp, ax_cdly_exp = plt.subplots()

df_dly_exp['cumm_dly_amount'].plot(marker='o', ax=ax_cdly_exp)

ax_cdly_exp.set_title('user cummulative daily expenses')

#%%
# =============================================================================
# DLY AND DLY CUMM INCOME
# =============================================================================

# ploting dly inc

fig_dly_inc, ax_dly_inc = plt.subplots()

df_dly_inc['dly_amount'].plot(marker='o', ax=ax_dly_inc)

ax_dly_inc.set_title('user daily income')

#%%

# ploting cumm dly inc

fig_cdly_inc, ax_cdly_inc = plt.subplots()

df_dly_inc['cumm_dly_amount'].plot(marker='o', ax=ax_cdly_inc)

ax_cdly_inc.set_title('user cummulative daily income')

#%%
# =============================================================================
# PLOTTING BALANCES dly and dly cumsum
# =============================================================================
df_dly_bal = daily_balances()


#%%
# ploting dly bal

fig_dly_bal, ax_dly_bal = plt.subplots()

df_dly_bal['dly_amount'].plot(marker='o', ax=ax_dly_bal)

ax_dly_bal.set_title('user daily balances')

#%%

# ploting cumm dly bal

fig_cdly_bal, ax_cdly_bal = plt.subplots()

df_dly_bal['cumm_dly_amount'].plot(marker='o', ax=ax_cdly_bal)

ax_cdly_bal.set_title('user cummulative daily balances')

#%%

# =============================================================================
# regplot
# =============================================================================

df_dly_bal.columns

sns.lineplot(data=df_dly_bal.reset_index(), 
            x='date', y='dly_amount_exp')



# =============================================================================
# END of ploting daily sums and cummulative sums over period
# =============================================================================

#%%

fig_exp, ax_exp = plt.subplots()

df_exp['base_amount'].plot(marker='o', ax=ax_exp)

ax_exp.set_title('user expenses')


#%%

fig_inc, ax_inc = plt.subplots()

df_inc['amount_cumm'].plot(marker='o')

ax_inc.set_title('user cummulative income')

#%%
fig_expcumm, ax_expcumm = plt.subplots()

df_exp['amount_cumm'].plot(marker='o', ax=ax_expcumm)

ax_expcumm.set_title('user cummulative  expenses')


#%%

fig_inccumm, ax_inccumm = plt.subplots()

df_inc['amount_cumm'].plot(marker='o')

ax_inccumm.set_title('user cummulative income')


#%%

# NO LOGS FOR NEGATIVE VALUES

#%%

# plot

def plot_df(df, x, y, title="", xlabel='date', ylabel='value', dpi=100):
    #plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, marker='o')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

#%%

plot_df(df_exp, x=df_exp.index, y=df_exp['base_amount'], 
        title='User expenses')

plot_df(df_inc, x=df_inc.index, y=df_inc['base_amount'], 
        title='User income')


#%%

reg = linear_model.LinearRegression()

# expenses

Y = [balance_dec,balance_jan,balance_feb]
reg.fit([[1],[2],[3]],Y)
reg.coef_
reg.intercept_
pred = reg.predict([[4]])
### Extracting prediction as integer ###
for i in pred:
    prediction = i

#plot the output#

X_values = np.array([1,2,3,4])
Y_values = np.array([balance_dec,balance_jan,balance_feb,prediction])
plt.scatter(X_values, Y_values, color="black", linewidth=3)
m, b = np.polyfit(X_values, Y_values, 1)
plt.plot(X_values, m*X_values+b, color="blue", linewidth=3)
plt.xlabel('months')
plt.ylabel('balance')
plt.title('Prediction')
fig1 = plt.gcf()
plt.show()

##save it as pdf and jpg##
now = datetime.now().strftime("%Y-%m-%d")
fig1.savefig(f'{now}_prediction.pdf')
fig1.savefig(f'{now}_prediction.jpg')





