import pandas as pd
data = pd.read_csv("../Data/creditcard.csv")
print(data.head())
print(data.info())
print(data.describe())
