import pandas as pd
import json
import datetime as dt


# with open('output.json', "r") as file:
#     data = json.load(file)
#
#     df = pd.read_csv('AR' + '_data.csv')
#     df['Date'] = pd.to_datetime(df['Date'])
#     df['plotting_date'] = pd.to_datetime(df['Date']).dt.date
#     df['Value $ '] = df['Balance'] * data['AR']['Current Price']
#     data['AR']['Current Value'] = df.iloc[-1:]['Value $ '].values[0]
#     grouped_day = df.groupby(pd.Grouper(key='Date', freq='1d'))['Balance'].mean().to_frame().dropna()
#     grouped_day= grouped_day.reset_index()
#     grouped_day['Date'] = df['Date'].dt.strftime('%d/%m')
#     # grouped_day.to_csv('AR_Daily_Balance.csv', columns=['plotting_date', 'Balance'], index = False)

df = pd.read_csv('docs/graphing/data/Totals_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
y = df.groupby(pd.Grouper(key='Date', freq='10min')).mean()
f = y.Balance.diff()
todays_gain = round(y.iloc[-2:]['Balance'].diff().values[1], 2)
# grouped_day = df.groupby(pd.Grouper(key = 'Date', freq='1D'))['Balance'].mean()
# grouped_day = grouped_day.dropna()
#
#
# grouped_hour = df.groupby(pd.Grouper(key = 'Date', freq='1H'))['Balance'].mean().to_frame()
# grouped_hour.columns = ['Balance Diff']
# grouped_hour = grouped_hour.dropna()
# grouped_hour['24 Hr Diff'] = grouped_hour['Balance Diff'].diff(periods = 4)
#
# df = pd.read_csv('Totals' + '_data.csv')
# df['Date'] = pd.to_datetime(df['Date'])
# y = df.groupby(pd.Grouper(key='Date', freq='1D'))['Total'].mean().to_frame()
# todays_gain = y.iloc[-1:]['Total'].values[0]