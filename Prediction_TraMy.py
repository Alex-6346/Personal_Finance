from sklearn import linear_model
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np


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

#month = pd.read_sql_query('''SELECT * FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('now', '-3 months') AND date('now') AND ti.user_id = "61730143"''', sqliteConnect)
df = pd.DataFrame(sql_query, columns = ['id', 'expense_date', 'group_id', 'subcategory_id', 'description', 'currency_code', 'repeat_interval', 'updated_date', 'id', 'transaction_id', 'user_id', 'amount', 'base_amount'])
print(df)
data = df[["expense_date", "subcategory_id", "base_amount"]]

#december = data[data['expense_date'].dt.strftime('%m') == '12'] to filter only december
#print(month)

#data['month'] = pd.DatetimeIndex(data["expense_date"]).month

def timestamp_change(x):
    y = datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
    return y

# Changing timestamp format #
# Gives a warning. Do not panic, it works #
data["expense_date"] = data["expense_date"].apply(timestamp_change)
# number of months
date1 = data["expense_date"][0]
date2 = data["expense_date"].iloc[-1]
num_months = math.ceil(((date1-date2)/np.timedelta64(1, 'M')))
#extracting month value
pd.DatetimeIndex(data["expense_date"]).month


#december
sum_expenses_dec = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '12' AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )
sum_income_dec = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '12' AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )

#january

sum_expenses_jan = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '01' AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )
sum_income_jan = sum_expenses_dec = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '01' AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )

#february

sum_expenses_feb = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '02' AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )
sum_income_feb = sum_expenses_dec = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions JOIN TransactionItems AS ti ON Transactions.id = ti.transaction_id WHERE user_id = 61730143 AND strftime('%m', expense_date) = '02' AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection )

### converting to data frame ###
exp_dec_df = pd.DataFrame(sum_expenses_dec, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])
inc_dec_df = pd.DataFrame(sum_income_dec, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])

exp_jan_df = pd.DataFrame(sum_expenses_jan, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])
inc_jan_df = pd.DataFrame(sum_income_jan, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])

exp_feb_df = pd.DataFrame(sum_expenses_feb, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])
inc_feb_df = pd.DataFrame(sum_income_feb, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)'])

##sum expenses and income in each month

total_exp_dec = exp_dec_df['sum(base_amount)'].sum()
total_inc_dec = inc_dec_df['sum(base_amount)'].sum()
balance_dec = total_inc_dec-total_exp_dec

total_exp_jan = exp_jan_df['sum(base_amount)'].sum()
total_inc_jan = inc_jan_df['sum(base_amount)'].sum()
balance_jan = total_inc_jan-total_exp_jan

total_exp_feb = exp_feb_df['sum(base_amount)'].sum()
total_inc_feb = inc_feb_df['sum(base_amount)'].sum()
balance_feb = total_inc_feb-total_exp_feb

### Linear Model ###
reg = linear_model.LinearRegression()
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
plt.plot(X_values, prediction, color="blue", linewidth=3)
plt.xlabel('months')
plt.ylabel('balance')
plt.title('Prediction')
fig1 = plt.gcf()
plt.show()

##save it as pdf and jpg##
now = datetime.now().strftime("%Y-%m-%d")
fig1.savefig(f'prediction_{now}.pdf')
fig1.savefig(f'prediction_{now}.jpg')
