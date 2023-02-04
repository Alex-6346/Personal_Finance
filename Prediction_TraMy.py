def run_prediction():
    """
    :return: balances of the previous 3 months and the prediction of the following month.
    balance_1, balance_2, balance_3, prediction
    """
    from sklearn import linear_model
    import sqlite3
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import math
    import matplotlib.pyplot as plt
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
    #december
    sum_expenses_dec = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02', '-2 months')  AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection)
    sum_income_dec = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02', '-2 months')  AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection)
    #january
    sum_expenses_jan = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-2 months') AND date('2023-03-02', '-1 months') AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection)
    sum_income_jan = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-2 months') AND date('2023-03-02', '-1 months') AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection)
    print(sum_income_jan)
    #february
    sum_expenses_feb = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-1 months') AND date('2023-03-02') AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id ''', sqliteConnection)
    sum_income_feb = pd.read_sql_query('''SELECT DISTINCT expense_date, subcategory_id, subcategory_name, sum(ABS(base_amount)) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-1 months') AND date('2023-03-02') AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''', sqliteConnection)
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
    return balance_dec, balance_jan, balance_feb, prediction

def plot_prediction(balance_1,balance_2,balance_3,prediction):
    """
    Takes the balance of the last three months and the prediction of the following month. Then it saves the plot as jpg
    and returns the name of the file and the figure of the plot
    :param balance_1
    :param balance_2
    :param balance_3
    :param prediction
    :return: name of plot file and figure of plot
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    #plot the output#
    X_values = np.array([1,2,3,4])
    Y_values = np.array([balance_1,balance_2,balance_3,prediction])
    plt.scatter(X_values, Y_values, color="black", linewidth=3)
    m, b = np.polyfit(X_values, Y_values, 1)
    plt.plot(X_values, m*X_values+b, color="blue", linewidth=3)
    plt.xlabel('months')
    plt.ylabel('balance')
    plt.title('Prediction')
    fig1 = plt.gcf()
    plt.show()
    now = datetime.now().strftime("%Y-%m-%d")
    name = f'{now}_prediction'
    return name, fig1
def save_plot_jpg(name, fig):
    fig.savefig(name + '.jpg')
def download_plot(name,fig):
    fig.savefig(name+'.pdf')


