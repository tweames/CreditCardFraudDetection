import numpy as np
import pandas as pd
def add_fraud(customer_profiles_table, terminal_profiles_table, transactions_df):
	
	# By default, all transactions are genuine
	transactions_df['TX_FRAUD'] = 0
	transactions_df['TX_FRAUD_SCENARIO'] = 0

	# Scenario 1: If transaction cost exceeds 220, it is a fraudulent transaction
	transactions_df.loc[transactions_df.TX_AMOUNT > 220, ['TX_FRAUD','TX_FRAUD_SCENARIO']] = 1
	nb_frauds_scenario_1=transactions_df.TX_FRAUD.sum()
	print("Number of frauds from scenario 1: "+str(nb_frauds_scenario_1))

	# Scenario 2: Randomly choose 2 terminals every day, 
	# all transactions at those terminals are fraudulent for the next 14 days
	# Simulates criminal use of a terminal such as phishing
	for day in  range(transactions_df.TX_TIME_DAYS.max()):
		# Randomly select two fraudulent terminals
		compromised_terminals = terminal_profiles_table.TERMINAL_ID.sample(n=2, random_state=day)
		
		# Transactions taking place at a fraudulent terminal in the last two weeks need to me marked as compromised
		compromised_transactions = transactions_df[(transactions_df.TX_TIME_DAYS>=day) &
		                                           (transactions_df.TX_TIME_DAYS < day + 14) & # Interval for fraud
                                                   (transactions_df.TERMINAL_ID.isin(compromised_terminals))]
		
		# Mark the transactions as fraudulent from Scenario 2
		transactions_df.loc[compromised_transactions.index, 'TX_FRAUD']=1
		transactions_df.loc[compromised_transactions.index, 'TX_FRAUD_SCENARIO']=2
	nb_frauds_scenario_2 = transactions_df.TX_FRAUD.sum() - nb_frauds_scenario_1
	print("Number of frauds from scenario 2: " +str(nb_frauds_scenario_2))

	# Scenario 3: Every day, a list of 3 customers are drawn at random. Over the course of 7 days 
	# 1/3 of their transactions are multipled by 5
	# Simulates card-not-present fraud
	temp = [0]
	for day in range(transactions_df.TX_TIME_DAYS.max()):
		# Randomly flag 3 customers
		compromised_customers = customer_profiles_table.CUSTOMER_ID.sample(n=3, random_state=day).values	
		# If a customer has been flagged in the last 7 days, mark transactions as compromised
		compromised_transactions=transactions_df[(transactions_df.TX_TIME_DAYS>=day) & 
                                                 (transactions_df.TX_TIME_DAYS<day+14) & 
                                                 (transactions_df.CUSTOMER_ID.isin(compromised_customers))]
	
		# Number of compromised transactions
		nb_compromised_transactions = compromised_transactions.shape[0]

        # Set seed for choosing 1/3 transactions to be multiplied by 5
		np.random.seed(day)
        
		# Randomly sample 1/3 of list in range(nb_compromised_transactions)
		index_fraud_temp = list(range(nb_compromised_transactions)) 
		np.random.shuffle(index_fraud_temp)
		index_fraud_temp = index_fraud_temp[:int(nb_compromised_transactions/3)]
		
		# TODO: Fix this line to use the label 'TRANSACTION_ID' instead of known position
		index_fraud = compromised_transactions.values[index_fraud_temp,0]
		
		transactions_df.loc[index_fraud,'TX_AMOUNT']=transactions_df.loc[index_fraud,'TX_AMOUNT']*5
		transactions_df.loc[index_fraud,'TX_FRAUD']=1
		transactions_df.loc[index_fraud,'TX_FRAUD_SCENARIO']=3
        
                             
	nb_frauds_scenario_3=transactions_df.TX_FRAUD.sum()-nb_frauds_scenario_2-nb_frauds_scenario_1
	print("Number of frauds from scenario 3: "+str(nb_frauds_scenario_3))
    
	return transactions_df
