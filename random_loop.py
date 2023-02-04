# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 23:27:59 2023

@author: calna
"""
import random as rand
from second_task import *
from datetime import datetime, date, timedelta 
from sql_currency import currency
import pandas as pd
import json

#%%

def access_to_splitwise():
    with open("settings.txt") as f:
        settings = json.load(f)

    s_obj = Splitwise(settings['splitwise_name'],
                      settings['splitwise_pass'],
                      api_key=settings['splitwise_key'])
    return s_obj

#%%

def random_inc_exp(inc_loops= 10, exp_loops= 25):
    
    s_obj = access_to_splitwise()
    user = s_obj.getCurrentUser()
    user_id = user.getId()
    
    try:
        conn = sqlite3.connect(str(user_id) + ".sqlite")
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
    except Error as e:
        print(e)
    
    with open ('currency_symbols.json','r') as f:
        symbols = json.load(f)       # load for reading json file f
    
    #dt_start = datetime(2022,12,1).date()
    dt_start = datetime(2022,12,1).date()
    
    dt_end = datetime.now().date()
    
    dt_range = [dt_start + timedelta(x) for x in range (int((dt_end-dt_start).days+1))]
    
    for x in range(int(inc_loops)):
        
        subcategory_id = rand.randint(101, 105)
        
        amount = rand.randint(500, 2000)
        
        #currency = rand.choice(symbols)
        
        date = rand.choice(dt_range)
        
        hour = rand.choice(range(0,24))
        
        min = rand.choice(range(0,60))
        
        sec = rand.choice(range(0,60))
        
        date_format = f'{date}T{hour}:{min}:{sec}Z'
        #date_format = str(date)+'T15:46:56Z'
        
        insert_transaction(conn, cursor, date_format, None, subcategory_id,
                           str(x) + 'random income', 'EUR', None)
        
        transaction_id = cursor.lastrowid
        insert_transaction_item(conn, cursor, transaction_id, 61730143, amount)
        
    for x in range(int(exp_loops)):
        
        #subcategory_id = rand.randint(101, 105)
        
        sub_ls = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23,
                  24,26,28,29,30,32,33,34,35,36,37,38,39,41,42,43,44,
                  45,46,47,48,49,50]
        
        subcategory_id = rand.choice(sub_ls)
        
        amount = rand.randint(50, 1000)
        
        currency = rand.choice(symbols)
        
        currency_trans = rand.choice([currency,'EUR','EUR'])
        
        date = rand.choice(dt_range)
        
        hour = rand.choice(range(0,24))
        
        min = rand.choice(range(0,60))
        
        sec = rand.choice(range(0,60))
        
        date_format = f'{date}T{hour}:{min}:{sec}Z'
        #date_format = "2022-12-20T15:46:56Z"
        
        insert_transaction(conn, cursor, date_format, None, subcategory_id,
                           str(x) + 'random expense', currency_trans, None)
        
        transaction_id = cursor.lastrowid
        insert_transaction_item(conn, cursor, transaction_id, 61730143, amount)
    
    print(f'\nEnter random {inc_loops} income and \
{exp_loops} expense transactions \nbetween dates {dt_start} , {dt_end} ')

#%%

def loop_control():
    """executes the random loop only once based on settings key[loop] value"""
    settings = pd.read_json('settings.txt', typ='series')
    
    check = 0
    
    if settings['loop'] != "1":
        
        settings['loop'] = "1"
        
        settings.to_json('settings.txt')
        
        check = check + 1
        
        random_inc_exp(20,60)
        
    print(f"\nRandom loop executed {check} times\n")
        

        
#%%

if __name__ == "__main__":

    # number of loop arguments: first income (1/5), second expenses (4/5), 
    #random_inc_exp(20, 40)
    loop_control()
    currency()


