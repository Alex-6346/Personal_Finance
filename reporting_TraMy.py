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
expenses = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02') AND ti.user_id = "61730143" AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''',sqliteConnect)
#income
income = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02') AND ti.user_id = "61730143" AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''',sqliteConnect)

#converting to dataframe
month1_exp_df = pd.DataFrame(month1_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
month2_exp_df = pd.DataFrame(month2_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
month3_exp_df = pd.DataFrame(month3_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
expenses_df = pd.DataFrame(expenses, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)', 'type'])
income_df = pd.DataFrame(income, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)', 'type'])


                                       ###creating pie chart last month###

#calculating percentage of each subcategory
tot_1 = month1_exp_df['sum(base_amount)'].sum()

def relative_value(x):
        y = x/tot_1
        return y*100

month1_exp_df['sum(base_amount)'] = month1_exp_df['sum(base_amount)'].apply(relative_value)

#creating list of "subcategory_name" and sum(base_mount)

list_sub_1 = month1_exp_df['subcategory_name'].tolist()
list_amount_1 = month1_exp_df['sum(base_amount)'].tolist()

#plot as pie chart
fig1, ax1 = plt.subplots()
pie_chart = ax1.pie(list_amount_1, labels = list_sub_1, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})

plt.title('Expenses last month')
plt.legend(title = "subcategory name:")
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

                                                ###creating pie chart 2 months ago###


#calculating percentage of each subcategory
tot_2 = month2_exp_df['sum(base_amount)'].sum()

def relative_value_2(x):
        y = x/tot_2
        return y*100

month2_exp_df['sum(base_amount)'] = month2_exp_df['sum(base_amount)'].apply(relative_value_2)

#creating list of "subcategory_name" and sum(base_mount)

list_sub_2 = month2_exp_df['subcategory_name'].tolist()
list_amount_2 = month2_exp_df['sum(base_amount)'].tolist()

#plot as pie chart
fig2, ax2 = plt.subplots()
pie_chart_2 = ax2.pie(list_amount_2, labels = list_sub_2, startangle=90, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
plt.title('Expenses two months ago')
plt.legend(title = "subcategory name:", loc = 'upper right', bbox_to_anchor=(0.05, 0.5))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

                                                                ###creating pie chart 3 months ago###



#calculating percentage of each subcategory
tot_3 = month3_exp_df['sum(base_amount)'].sum()

def relative_value_3(x):
        y = x/tot_3
        return y*100

month3_exp_df['sum(base_amount)'] = month3_exp_df['sum(base_amount)'].apply(relative_value_3)

#creating list of "subcategory_name" and sum(base_mount)

list_sub_3 = month3_exp_df['subcategory_name'].tolist()
list_amount_3 = month3_exp_df['sum(base_amount)'].tolist()

#plot as pie chart
fig3, ax3 = plt.subplots()
pie_chart_3, texts = ax3.pie(list_amount_3, labels = list_sub_3, startangle=90, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
plt.title('Expenses three months ago')
plt.legend(title = "subcategory name:", loc = 'upper right', bbox_to_anchor=(0.05, 0.5))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

                                            ##creating bar chart expenses vs. income###


expenses_df = pd.DataFrame(expenses, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
income_df = pd.DataFrame(income, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])

#find out sum of expenses and income to create dataset
total_income = abs(income_df['sum(base_amount)'].sum()) #takings absolute value because of fact balance
total_expenses = abs(expenses_df['sum(base_amount)'].sum())

category = ['income', 'expenses']
values = [total_income, total_expenses]

fig = plt.figure(figsize = (5, 5))
plt.bar(category, values, color ='maroon',width = 0.5)
plt.xlabel('category')
plt.ylabel('amount in €')
plt.title('income vs. expenses in last 3 months')

plt.show()