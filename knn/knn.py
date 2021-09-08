import pandas as pd


nomecsv = 'teste.csv'

data = pd.read_csv(nomecsv)

percent = int(data.shape[0] * 0.6)

train = data.iloc[:percent, :]
test = data.iloc[percent:, :]


a=1
