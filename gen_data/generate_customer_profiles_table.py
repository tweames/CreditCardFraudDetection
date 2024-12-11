import numpy as np
import pandas as pd
def generate_customer_profiles_table(n_customers, random_state=0):

	# Initialize random seed
	np.random.seed(random_state)

	# Initialize customer table
	customer_id_properties=[]

	# Generate customer properties from random distributions
	for customer_id in range(n_customers):
	
		# Initialize x and y coordinate of customer
		x_customer_id = np.random.uniform(0,100)
		y_customer_id = np.random.uniform(0,100)

		# Initialize mean expenditure vale and standard deviation (values are arbitrary, but sensible)
		mean_amount = np.random.uniform(5,100)
		std_amount = mean_amount/2

		# Initialize mean number of transactions per day
		mean_nb_tx_per_day = np.random.uniform(0,4)

		customer_id_properties.append([customer_id,
									x_customer_id, y_customer_id,
									mean_amount, std_amount,
									mean_nb_tx_per_day])

	# Insert customer data into pandas dataframe
	customer_profiles_table = pd.DataFrame(customer_id_properties, columns = ['CUSTOMER_ID', 'x_customer_id', 'y_customer_id', 'mean_amount', 'std_amount', 'mean_nb_tx_per_day'])

	return customer_profiles_table
