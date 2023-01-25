from sklearn import linear_model
import sqlite3
import numpy as np
import pandas as pd
import datetime
import math


try:
    sqliteConnection = sqlite3.connect("61730143.sqlite") #connect with database
    cursor = sqliteConnection.cursor()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


try:

 cursor.execute("SELECT * FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143") #join tables and filter only Max
 remaining_rows = cursor.fetchall()

except sqlite3.IntegrityError as err:
    print(err)

sql_query = pd.read_sql_query('''SELECT * FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143''', sqliteConnection )

df = pd.DataFrame(sql_query, columns = ['id', 'expense_date', 'group_id', 'subcategory_id', 'description', 'currency_code', 'repeat_interval', 'updated_date', 'id', 'transaction_id', 'user_id', 'amount', 'base_amount'])

data = df[["expense_date", "subcategory_id", "base_amount"]]

#december = data[data['expense_date'].dt.strftime('%m') == '12'] to filter only december
#print(month)

#data['month'] = pd.DatetimeIndex(data["expense_date"]).month

def timestamp_change(x):
    y = datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
    return y

# Changing timestamp format #
data["expense_date"].apply(timestamp_change)
# number of months
date1 = data["expense_date"][0]
date2 = data["expense_date"].iloc[-1]
num_months = math.ceil(((date1-date2)/np.timedelta64(1, 'M')))
#extracting month value
pd.DatetimeIndex(data["expense_date"]).month

#Obtaining balances
balance_feb = 0
balance_jan = 0
balance_dec =0
for i in [2,1,12] :
    temp = data[data['expense_date'].dt.strftime('%m') == i]
    for row in temp:
        if ['subcategory_id']