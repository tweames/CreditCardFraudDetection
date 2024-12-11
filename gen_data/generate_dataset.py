import generate_customer_profiles_table as gen_cust # Generates customers
import generate_terminal_profiles_table as gen_term	# Generates Terminals
import get_list_terminals_within_radius as get_term # lists terminals within radius of customer
import generate_transactions_table as gen_tx # Generates Transactions
import pandas as pd
from  multiprocessing import Pool
import time as time
def generate_dataset(n_customers = 5, n_terminals = 5, start_date = "2018-04-01", nb_days = 10, r = 50):

	# This file generates customer dataset with transactions

	# Initialize pandarallel
	#pandarallel.initialize(use_memory_fs=False,nb_workers=4,progress_bar=True) 	

	# Generate customer profiles
	start_time=time.time()
	customer_profiles_table = gen_cust.generate_customer_profiles_table(n_customers,random_state=0)
	print("Time to generate customer profiles table :{0:.2}s".format(time.time()-start_time))	
	
	# Generate terminal profiles
	start_time = time.time()
	terminal_profiles_table = gen_term.generate_terminal_profiles_table(n_terminals,random_state=0)
	print("Time to generate terminal profiles table :{0:.2}s".format(time.time()-start_time))	

	# Find terminals in range of customers using parallel processing 
	start_time = time.time()
	x_y_terminals = terminal_profiles_table[['x_terminal_id','y_terminal_id']].values.astype(float)
	pool = Pool()	
	customer_profiles_table['available_terminals'] = customer_profiles_table.apply(lambda x : get_term.get_list_terminals_within_radius(x, x_y_terminals=x_y_terminals, r=50),axis=1)
	print("Time to find available terminals:{0:.2}s".format(time.time()-start_time))

	# Time to generate transactions for customers using parallel apply
	start_time = time.time()
	transactions_df=customer_profiles_table.groupby('CUSTOMER_ID').apply(lambda x : gen_tx.generate_transactions_table(x.iloc[0], nb_days=nb_days)).reset_index(drop=True)
	#transactions_df=pool.apply_async(customer_profiles_table.groupby('CUSTOMER_ID').apply(lambda x : gen_tx.generate_transactions_table(x.iloc[0], nb_days=5)).reset_index(drop=True), customer_profiles_table)
	print("Time to generate transaction tables:{0:.2}s".format(time.time()-start_time))	

	# Sort transactions chronologically
	transactions_df = transactions_df.sort_values('TX_DATETIME')
	# Reset indices, starting from 0
	transactions_df.reset_index(inplace=True,drop=True)
	transactions_df.reset_index(inplace=True)
	# TRANSACTION_ID are the dataframe indices, starting from 0
	transactions_df.rename(columns = {'index':'TRANSACTION_ID'}, inplace = True)

	return (customer_profiles_table, terminal_profiles_table, transactions_df)

