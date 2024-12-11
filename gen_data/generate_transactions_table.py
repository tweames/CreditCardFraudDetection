import numpy as np
import pandas as pd
def generate_transactions_table(customer_profile, start_date = "2018-04-01", nb_days = 10):

	# This file generates the transaction table for a customer profile over a given number of days

	# Initialize customer transaction list
	customer_transactions = []

	# Initialize random seed
	np.random.seed(int(customer_profile.CUSTOMER_ID))
	np.random.seed(int(customer_profile.CUSTOMER_ID))

	# For number of days, generate list of transactions
	for day in range(nb_days):
		
		# Random number of transactions for that day
		nb_tx = np.random.poisson(customer_profile.mean_nb_tx_per_day)

		# If nb_tx is positive, then generate transactions
		if nb_tx > 0:
			
			# For number of transactions
			for tx in range(nb_tx):

				# Randomly sample transactions around 2pm with standard deviation of 4 hours
				time_tx = int(np.random.normal(50400, 14400))

				# If the transaction time given lies in the range of seconds in a day keep it
				if (time_tx > 0) and (time_tx<86400):
				
					# Transaction amount is drawn from a normal distribution
					amount = np.random.normal(customer_profile.mean_amount, customer_profile.std_amount)
				
					# If amount is negative, draw from a uniform distribution instead
					if amount < 0:
					# Consider the uniform distribution to be from 0 to the customer mean amount and 3 standard deviations
						amount = np.random.uniform(0, customer_profile.mean_amount + 3*customer_profile.std_amount)

					# Round to the nearest cent
					amount = np.round(amount,decimals=2)

					# If there is an available terminal neraby, choose the terminal the customer withdraws from

					if len(customer_profile.available_terminals) > 0:
						# Randomly choose terminal from set of available terminals
						terminal_id = np.random.choice(customer_profile.available_terminals)
						
						# Append information to customer transactions
						customer_transactions.append([time_tx+day*86400, day, customer_profile.CUSTOMER_ID, terminal_id, amount])

	customer_transactions = pd.DataFrame(customer_transactions, columns=['TX_TIME_SECONDS', 'TX_TIME_DAYS', 'CUSTOMER_ID', 'TERMINAL_ID', 'TX_AMOUNT'])
    
	if len(customer_transactions)>0:
		customer_transactions['TX_DATETIME'] = pd.to_datetime(customer_transactions["TX_TIME_SECONDS"], unit='s', origin=start_date)
		customer_transactions=customer_transactions[['TX_DATETIME','CUSTOMER_ID', 'TERMINAL_ID', 'TX_AMOUNT','TX_TIME_SECONDS', 'TX_TIME_DAYS']]
    
	return customer_transactions 
