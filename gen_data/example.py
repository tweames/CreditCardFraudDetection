import pandas as pd
import os
import datetime
import generate_customer_profiles_table as gen_cust # Generates customers
import generate_terminal_profiles_table as gen_term	# Generates Terminals
import get_list_terminals_within_radius as get_term # lists terminals within radius of customer
import generate_transactions_table as gen_tx # Generates Transactions
import add_fraud
import fraud_and_transactions_stats_fig as fraud_fig
n_customers = 5000
n_terminals = 10000
nb_days = 183
customer_profiles_table = gen_cust.generate_customer_profiles_table(n_customers,random_state=0)
terminal_profiles_table = gen_term.generate_terminal_profiles_table(n_terminals,random_state=0)
x_y_terminals = terminal_profiles_table[['x_terminal_id','y_terminal_id']].values.astype(float)
customer_profiles_table['available_terminals'] = customer_profiles_table.apply(lambda x : get_term.get_list_terminals_within_radius(x, x_y_terminals=x_y_terminals, r=50),axis=1)
transactions_df=customer_profiles_table.groupby('CUSTOMER_ID').apply(lambda x : gen_tx.generate_transactions_table(x.iloc[0], nb_days=nb_days)).reset_index(drop=True)	
transactions_df = transactions_df.sort_values('TX_DATETIME')
# Sort transactions chronologically
transactions_df=transactions_df.sort_values('TX_DATETIME')
# Reset indices, starting from 0
transactions_df.reset_index(inplace=True,drop=True)
transactions_df.reset_index(inplace=True)
# TRANSACTION_ID are the dataframe indices, starting from 0
transactions_df.rename(columns = {'index':'TRANSACTION_ID'}, inplace = True)
transactions_df = add_fraud.add_fraud(customer_profiles_table, terminal_profiles_table, transactions_df)
print("Percentage of fraudulent transactions: " + str(transactions_df.TX_FRAUD.mean()))
print("Number of fraudulent transactions: " + str(transactions_df.TX_FRAUD.sum()))
fraud_fig.fraud_and_transactions_stats_fig(transactions_df)


# Save simulated data
DIR_OUTPUT = "./simulated-data-raw/"

# Check if path exists, if not make path
if not os.path.exists(DIR_OUTPUT):
    os.makedirs(DIR_OUTPUT)

# TODO: Fix this for date put into generate data function
start_date = datetime.datetime.strptime("2018-04-01", "%Y-%m-%d")

for day in range(transactions_df.TX_TIME_DAYS.max()+1):

    transactions_day = transactions_df[transactions_df.TX_TIME_DAYS==day].sort_values('TX_TIME_SECONDS')

    date = start_date + datetime.timedelta(days=day)
    filename_output = date.strftime("%Y-%m-%d")+'.pkl'

    # Protocol=4 required for Google Colab
    transactions_day.to_pickle(DIR_OUTPUT+filename_output, protocol=4)
