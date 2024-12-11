import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
def get_stats(transactions_df):
	# Number of transactions per day
	nb_tx_per_day = transactions_df.groupby(['TX_TIME_DAYS'])['CUSTOMER_ID'].count()
	
	# Number of fraudulent transactions per day
	nb_fraud_tx_per_day = transactions_df.groupby(['TX_TIME_DAYS'])['TX_FRAUD'].sum()
	
	# Number of fraudulent cards per day
	nb_fraudcard_per_day = transactions_df[transactions_df['TX_FRAUD']>0].groupby(['TX_TIME_DAYS']).CUSTOMER_ID.nunique()
	
	return (nb_tx_per_day,nb_fraud_tx_per_day,nb_fraudcard_per_day)

def fraud_and_transactions_stats_fig(transactions_df):
	# Call get_stats
	(nb_tx_per_day,nb_fraud_per_day,nb_fraudcard_per_day)=get_stats(transactions_df)

	# Get number of days
	n_days=len(nb_tx_per_day)
	
	# Make transaction stats dataframe with values from get_stats
	tx_stats=pd.DataFrame({"value":pd.concat([nb_tx_per_day/100,nb_fraud_per_day,nb_fraudcard_per_day])})

	# First values are # transactions per day, etc  
	tx_stats['stat_type']=["nb_tx_per_day"]*n_days+["nb_fraud_per_day"]*n_days+["nb_fraudcard_per_day"]*n_days
	tx_stats=tx_stats.reset_index()
	
	# Use seaborn for plots
	
	# Figure parameters
	sns.set(style='darkgrid')
	sns.set(font_scale=1.4)
	fraud_and_transactions_stats_fig = plt.gcf()
	fraud_and_transactions_stats_fig.set_size_inches(15, 8)
	
	# Plot # of transactions per day
	sns.lineplot(x="TX_TIME_DAYS", y="value", data=tx_stats[tx_stats["stat_type"] == "nb_tx_per_day"], color = 'blue', label='# transactions per day')

	# Plot # of fraudulent transactions per day
	sns.lineplot(x="TX_TIME_DAYS", y="value", data=tx_stats[tx_stats["stat_type"] == "nb_fraud_per_day"], color = 'green', label='# fraudulent transactions per day (/100)')
	
	# Plot # fraudulent cards per day
	sns.lineplot(x="TX_TIME_DAYS", y="value", data=tx_stats[tx_stats["stat_type"] == "nb_fraudcard_per_day"], color = 'orange', label='# fraudulent cards per day')
	
	# Plot title, labels, legend, and show
	plt.title('Total transactions, and number of fraudulent transactions \n and number of compromised cards per day', fontsize=20)
	plt.xlabel("Number of days since beginning of data generation")
	plt.ylabel("Number of:")
	plt.ylim(0,tx_stats["value"].max()+100)	
	plt.legend(loc='upper left')
	plt.show()
