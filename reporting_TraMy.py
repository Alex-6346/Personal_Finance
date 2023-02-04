import sqlite3
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

#%%

def pie_plot(df, value=5):
    
    df.loc[df['sum(base_amount)'] > value,'Subcategory'] = df['subcategory_name']
    
    df['Subcategory'].fillna('All Others',inplace=True)
    
    df_pie = df.groupby('Subcategory')[
            'sum(base_amount)'].sum().sort_values(ascending=False).reset_index()

    
    list_sub_1 = df_pie['Subcategory'].tolist()
    list_amount_1 = df_pie['sum(base_amount)'].tolist()

    
    return list_amount_1, list_sub_1


#%%
def report():

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
    #expenses
    expenses = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02') AND ti.user_id = "61730143" AND subcategory_id NOT BETWEEN 101 AND 105 GROUP BY subcategory_id''',sqliteConnect)
    #income
    income = pd.read_sql_query('''SELECT expense_date, subcategory_id, sum(base_amount) FROM Transactions AS t INNER JOIN TransactionItems AS ti ON t.id = ti.transaction_id INNER JOIN Subcategories as s ON s.id = t.subcategory_id WHERE expense_date BETWEEN date('2023-03-02', '-3 months') AND date('2023-03-02') AND ti.user_id = "61730143" AND subcategory_id BETWEEN 101 AND 105 GROUP BY subcategory_id''',sqliteConnect)
    
    #converting to dataframe
    month1_exp_df = pd.DataFrame(month1_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
    month2_exp_df = pd.DataFrame(month2_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
    month3_exp_df = pd.DataFrame(month3_exp, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
    expenses_df = pd.DataFrame(expenses, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)', 'type'])
    income_df = pd.DataFrame(income, columns = ['expense_date', 'subcategory_id', 'sum(base_amount)', 'type'])
    
    # Create a PDF file for the plots

    fig, ax= plt.subplots(2,2, figsize=(9,6))
    
    fig.axes
    
    
                                                              ###creating pie chart last month###
    
    #calculating percentage of each subcategory
    tot_1 = month1_exp_df['sum(base_amount)'].sum()
    
    def relative_value(x):
            y = x/tot_1
            return y*100

    
    month1_exp_df['sum(base_amount)'] = month1_exp_df['sum(base_amount)'].apply(relative_value)
    
    month1_exp_df.columns
    """    
    month1_exp_df.loc[month1_exp_df[
        'sum(base_amount)']>5,'Subcategory'] = month1_exp_df['subcategory_name']
    
    month1_exp_df['Subcategory'].fillna('Rest of Categories',inplace=True)
    
    month1_pie = month1_exp_df.groupby(
        'subcat_label')[
            'sum(base_amount)'].sum().sort_values(ascending=False).reset_index()
    
    #creating list of "subcategory_name" and sum(base_mount)
    
    list_sub_1 = month1_exp_df['subcategory_name'].tolist()
    list_amount_1 = month1_exp_df['sum(base_amount)'].tolist()
    
    labels_1 = [f'{l}, {s:0.1f}%' for l, s in zip(list_sub_1, list_amount_1)]
    """
    
    list_amount_1, labels_1 = pie_plot(month1_exp_df)
    
    #plot as pie chart
    ax[0,0].pie(list_amount_1, labels = labels_1, startangle=90,
                wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
                autopct='%1.0f%%', colors=sns.color_palette('Set2'))
                #textprops=dict(color='white')
    ax[0,0].set_title('Expenses last month')

    
                                                                   ###creating pie chart 2 months ago## 
    #calculating percentage of each subcategory
    tot_2 = month2_exp_df['sum(base_amount)'].sum()
    
    def relative_value_2(x):
            y = x/tot_2
            return y*100
    
    month2_exp_df['sum(base_amount)'] = month2_exp_df['sum(base_amount)'].apply(relative_value_2)
    '''    
    #creating list of "subcategory_name" and sum(base_mount)
    
    list_sub_2 = month2_exp_df['subcategory_name'].tolist()
    list_amount_2 = month2_exp_df['sum(base_amount)'].tolist()
    
    labels_2 = [f'{l}, {s:0.1f}%' for l, s in zip(list_sub_2, list_amount_2)]
    '''    
  
    list_amount_2, labels_2 = pie_plot(month2_exp_df)
    
    #plot as pie chart
    ax[0,1].pie(list_amount_2, labels = labels_2, startangle=90,
                wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
                autopct='%1.0f%%', colors=sns.color_palette('Set2'))
                #textprops=dict(color='white')
    ax[0,1].set_title('Expenses two months ago')
    #ax[0,1].legend(title = "subcategory name:", loc = 'upper right', bbox_to_anchor=(0.2, 0.5))
    #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #pie2 = plt.gcf()
    
    #save the pie chart
    #pie2.savefig(f'{now}_pie2.jpg')
    #pp.savefig()
    
    
                                                                                    ###creating pie chart 3 months ago###
    
    
    #calculating percentage of each subcategory
    tot_3 = month3_exp_df['sum(base_amount)'].sum()
    
    def relative_value_3(x):
            y = x/tot_3
            return y*100
    
    month3_exp_df['sum(base_amount)'] = month3_exp_df['sum(base_amount)'].apply(relative_value_3)

    
    ##creating list of "subcategory_name" and sum(base_mount)
    '''
    list_sub_3 = month3_exp_df['subcategory_name'].tolist()
    list_amount_3 = month3_exp_df['sum(base_amount)'].tolist()
    
    labels_3 = [f'{l}, {s:0.1f}%' for l, s in zip(list_sub_3, list_amount_3)]
    '''    
    
    list_amount_3, labels_3 = pie_plot(month3_exp_df)
    
    #colours = dict(zip(list_sub_3, plt.cm.tab20.colors[:len(list_sub_3)]))
    #plot as pie chart
    ax[1,0].pie(list_amount_3, labels = labels_3, startangle=90,
                wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
                autopct='%1.0f%%', colors=sns.color_palette('Set2'))
                #textprops=dict(color='white')
    ax[1,0].set_title('Expenses three months ago')
    
    #ax[1,0].get_legend
    
    #ax[1,0].legend(title = "subcategory name:", loc = 'best', bbox_to_anchor=(0.05, 0.5), prop={'size':8})
    
    
    
    #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #pie3 = plt.gcf()
    
    #save the pie chart
    #pie3.savefig(f'{now}_pie3.jpg')
    #pp.savefig()
    #plt.show()
    
    
    
    
    ##creating bar chart expenses vs. income###
    
    
    expenses_df = pd.DataFrame(expenses, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
    income_df = pd.DataFrame(income, columns = ['expense_date', 'subcategory_id', 'subcategory_name', 'sum(base_amount)'])
    
    #find out sum of expenses and income to create dataset
    total_income = abs(income_df['sum(base_amount)'].sum()) #takings absolute value because of fact balance
    total_expenses = abs(expenses_df['sum(base_amount)'].sum())
    
    category = ['income', 'expenses']
    values = [total_income, total_expenses]
    
    #fig = plt.figure(figsize = (5, 5))
    #axs[1,1].bar(category, values, color ='maroon',width = 0.5)
    
    ax[1,1].bar(category, values, color=sns.color_palette('Set2'), width = 0.7)
    ax[1,1].set_xlabel('category')
    ax[1,1].set_ylabel('amount in €')
    ax[1,1].set_title('income vs. expenses in last 3 months')
    #bar = plt.gcf()
    
    # 
    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    
    fig.savefig('pie_charts.jpg', format='jpg')
    
    #fig.savefig('pie_charts.pdf', format='pdf')


    return fig

#%%

def save_pie():
    
    fig = report()
    
    fig.savefig(f'pie_charts_{datetime.now().strftime("%m%d%Y_%H%M%S")}.pdf', format='pdf')

    #fig.savefig('pie_charts'+datetime.now().strftime("%m/%d/%Y_%H/%M/%S")+'.pdf', format='pdf')

#%%

if __name__ == "__main__":

    fig = report()
    
    save_pie()

#%%
