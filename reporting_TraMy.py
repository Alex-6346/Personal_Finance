import sqlite3
from datetime import datetime, date

import pandas as pd
import matplotlib.pyplot as plt

try:
    sqliteConnect = sqlite3.connect("61730143.sqlite")
    cursor = sqliteConnect.cursor()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


#last month
month1_exp = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-1 months') AND date('2023-03-02') AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnect)
#last 2 months
month2_exp = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-2 months') AND date('2023-03-02', '-1 months') AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnect)
#last 3 months
month3_exp = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02', '-2 months')  AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnect)
#repeating expenses
repeat = pd.read_sql_query('''SELECT DISTINCT expense_date, repeat_interval, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE  repeat_interval = "monthly" GROUP BY subcategory_id''', sqliteConnect)
#income
income = pd.read_sql_query( '''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE subcategory_id BETWEEN '101' AND '105' AND ti.user_id = "61730143"''',sqliteConnect)

#converting to dataframe
month1_exp_df = pd.DataFrame(month1_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
month2_exp_df = pd.DataFrame(month2_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
month3_exp_df = pd.DataFrame(month3_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
repeat_df = pd.DataFrame(repeat, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
income_df = pd.DataFrame(income, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])

###creating pie chart last month###

#calculating percentage of each subcategory
tot = month1_exp_df['sum(base_amount)'].sum()

def relative_value(x):
        y = x/tot
        return y*100

month1_exp_df['sum(base_amount)'] = month1_exp_df['sum(base_amount)'].apply(relative_value)

#creating list of "subcategory_name" and sum(base_mount)

list_sub = month1_exp_df['subcategory_name'].tolist()
list_amount = month1_exp_df['sum(base_amount)'].tolist()

#plot as pie chart
fig1, ax1 = plt.subplots()
ax1.pie(list_amount, labels = list_sub, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()






