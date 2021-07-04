import pandas as pd

df = pd.read_csv('AR_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
grouped_day = df.groupby(pd.Grouper(key = 'Date', freq='1D'))['Balance'].mean()
grouped_day = grouped_day.dropna()


grouped_hour = df.groupby(pd.Grouper(key = 'Date', freq='1H'))['Balance'].mean().to_frame()
grouped_hour.columns = ['Balance Diff']
grouped_hour = grouped_hour.dropna()
grouped_hour['24 Hr Diff'] = grouped_hour['Balance Diff'].diff(periods = 4)