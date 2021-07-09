import pandas as pd
import json
import datetime as dt
import matplotlib.pyplot as plt
from selenium import webdriver
import time

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

# df = pd.read_csv('docs/graphing/data/Totals_data.csv')
# df['Date'] = pd.to_datetime(df['Date'])
# y = df.groupby(pd.Grouper(key='Date', freq='10min')).mean()
# f = y.Balance.diff()
# todays_gain = round(y.iloc[-2:]['Balance'].diff().values[1], 2)
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

# df = pd.read_csv('docs/graphing/data/AR_data.csv')
# df['Date'] = pd.to_datetime(df['Date'])
# grouped = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()
# diff = (grouped['Balance'].pct_change().values[-1] * 100)
# grouped = grouped.reset_index()
# # grouped['Date'] = grouped['Date'].dt.strftime('%d/%m')
# grouped['%'] = grouped['Balance'].pct_change(periods=1)
# plt.plot(grouped['Date'], grouped['%'] * 100)
# plt.show()


import json

with open('output.json') as jsonFile:
    jsonObject = json.load(jsonFile)

df = pd.read_csv('docs/graphing/data/Totals_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
y = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()
df['Date'] = df['Date'].dt.strftime('%d/%m')

todays_gain_pct = (y['Balance'].pct_change().values[-1]) * 100
todays_gain = y.iloc[-2:]['Balance'].diff()

new_df = y['Balance'].diff().round(2)
new_df = new_df.reset_index()
new_df['Date'].dt.strftime('%d/%m')
new_df.to_csv('daily_gains.csv', index=False)

# import coinmarketcapapi
# storage = {
#     "XCH": {
#         "Current Price": 0,
#         "Current Balance": 0.18825,
#         "Wallet Balance": 0.14048,
#         "Collateral Balance": 0.04776,
#         "Current Value": 0.0,
#         "Average Daily Increase": 0.00019,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "5.12%"
#     },
#     "XFX": {
#         "Current Price": 0,
#         "Current Balance": 4.32541,
#         "Wallet Balance": 2.75,
#         "Collateral Balance": 1.57541,
#         "Current Value": 0.0,
#         "Average Daily Increase": 0.00726,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "7.52%"
#     },
#     "CGN": {
#         "Current Price": 0,
#         "Current Balance": 6000.0,
#         "Current Value": 0.0,
#         "Average Daily Increase": 8.06452,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "-17.28%"
#     },
#     "SPARE": {
#         "Current Price": 0,
#         "Current Balance": 28.0,
#         "Current Value": 0.0,
#         "Average Daily Increase": 0.06452,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "-16.85%"
#     },
#     "AR": {
#         "Current Price": 0,
#         "Current Balance": 0.06678,
#         "Hashrate": "0.00",
#         "Current Value": 0.0,
#         "Average Daily Increase": 0.00016,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "7.17%"
#     },
#     "SIT": {
#         "Current Price": 0,
#         "Current Balance": 4.0,
#         "Current Value": 0.0,
#         "Average Daily Increase": 0.02941,
#         "Average Daily Value Increase": 0.0,
#         "Daily % Change": "35.29%"
#     },
#     "Totals": {
#         "Total": 0.0,
#         "Today's Gain $": 1.324,
#         "Today's % Gain": 3.0
#     }
# }
# cmc_api_key = 'a98e9495-0d8f-438b-8691-cb08d162cd59'
# cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
# data = cmc.cryptocurrency_quotes_latest(symbol='XCH', convert='USD').data
# storage['XCH']['Current Price'] = round(data['XCH']['quote']['USD']['price'], 2)
# change = str(round(data['XCH']['quote']['USD']['percent_change_24h'], 2)) + '%'
# storage['XCH']['24hr Price Change'] = change
# options = webdriver.ChromeOptions()
# # options.add_argument('headless')
# # options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome('./chromedriver', options=options)
# driver.get('https://chia-og.foxypool.io/my-farmer')
# driver.minimize_window()
# pool_key_input = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/input')
# pool_key_input.send_keys(
# #     '8cae91ac66fd08959589339242980a88336bbb201c75a38cda84e32f1e4e1db06cbb52e2c7c57242528acab832ace197')
# # login_button = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/button')
# # login_button.click()
# # time.sleep(1.5)
# # EC = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[1]/div[3]/div/div[2]')
#
# import yfinance as yf
# df = pd.read_csv('docs/graphing/data/XCH_data.csv')
# df['Date'] = pd.to_datetime(df['Date'])
# df['Balance_Diff'] = df['Balance'].diff()
# grouped = df.groupby(pd.Grouper(key='Date', freq='d'))['Balance_Diff'].sum()
# plotting_path = 'docs/graphing/data/'
# with open('output.json', "r") as file:
#     data = json.load(file)
# for token in data.keys():
#     USD_GBP = yf.download('GBPUSD=X', period='1d', interval='1h')
#     exchange = USD_GBP['Close'][-1]
#     df = pd.read_csv(plotting_path + token + '_data.csv')
#     df['Date'] = pd.to_datetime(df['Date'])
#     df['% Change_in_Balance'] = (df.Balance.pct_change(periods=12)) * 100
#     df['Balance_Diff'] = df.Balance.diff()
#     df['Value_Dollars'] = df['Balance'] * data[token]['Current Price']
#     df['Value_Pounds'] = df['Value_Dollars'] / exchange
#     df['Change_in_Value'] = df['Balance_Diff'] * df['Price']
#
#     x = df.groupby(pd.Grouper(key='Date', freq='1h'))['Balance_Diff'].sum()
#     y = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance_Diff'].sum()
#     z = df.groupby(pd.Grouper(key='Date', freq='1W'))['Balance_Diff'].sum()
#     p = df.groupby(pd.Grouper(key='Date', freq='1M'))['Balance_Diff'].sum()
#     grouped_daily = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()
#
#     average_hourly_difference = round(x.mean(), 5)
#     average_hourly_dollar_gainz = round(average_hourly_difference * data[token]['Current Price'], 2)
#
#     diff = (grouped_daily['Balance'].pct_change().values[-1] * 100)
#     average_daily_difference = round(y.mean(), 5)
#     average_daily_dollar_gainz = round(average_daily_difference * data[token]['Current Price'], 2)
#
#     average_weekly_difference = round(z.mean(), 5)
#     average_weekly_dollar_gainz = round(average_weekly_difference * data[token]['Current Price'], 2)
#
#     average_monthly_difference = round(p.mean(), 5)
#     average_monthly_dollar_gainz = round(average_monthly_difference * data[token]['Current Price'], 2)
#
#     # data[token]['Average Hourly Increase'] = average_hourly_difference
#     # data[token]['Average Hourly Value Increase'] = average_hourly_dollar_gainz
#     data[token]['Current Value'] = '$' + str(round(df.iloc[-1:]['Value_Dollars'].values[0], 2))
#     data[token]['Average Daily Increase'] = str(average_daily_difference) + ' ' + token
#     data[token]['Average Daily Value Increase'] = '$' + str(average_daily_dollar_gainz)
#     data[token]['Daily % Change'] = str(round(diff, 2)) + '%'

import requests
import ast


x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
blocks = x.split(';;')

for block in blocks[:-1]:
    x = json.loads(block)



import pandas as pd
import json
import yfinance as yf
import math
todays_gain = 0
todays_gain_pct = 0
plotting_path = 'docs/graphing/data/'
# with open('output.json', "r") as file:
#     data = json.load(file)
# for token in data.keys():
#     if token != 'Totals':
#
#         USD_GBP = yf.download('GBPUSD=X', period='1d', interval='1h')
#         exchange = USD_GBP['Close'][-1]
#         df = pd.read_csv(plotting_path + token + '_data.csv')
#         df['Date'] = pd.to_datetime(df['Date'])
#         df['% Change_in_Balance'] = (df.Balance.pct_change(periods=12)) * 100
#         df['Balance_Diff'] = df.Balance.diff()
#         df['Value_Dollars'] = df['Balance'] * data[token]['Current Price']
#         df['Value_Pounds'] = df['Value_Dollars'] / exchange
#         df['Change_in_Value'] = df['Balance_Diff'] * df['Price']
#
#         x = df.groupby(pd.Grouper(key = 'Date', freq='1h'))['Balance_Diff'].sum()
#         y = df.groupby(pd.Grouper(key = 'Date', freq='1D'))['Balance_Diff'].sum()
#         z = df.groupby(pd.Grouper(key = 'Date', freq='1W'))['Balance_Diff'].sum()
#         p = df.groupby(pd.Grouper(key = 'Date', freq='1M'))['Balance_Diff'].sum()
#         grouped_daily = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()
#
#
#
#         average_hourly_difference = round(x.mean(), 5)
#         average_hourly_dollar_gainz = round(average_hourly_difference * data[token]['Current Price'], 2)
#
#         # grouped_hourly = df.groupby(pd.Grouper(key= 'Date', freq='1h'))['Balance']
#
#         diff = (grouped_daily['Balance'].pct_change().values[-1] * 100)
#         hourly_diff = df.iloc[-49:]['Balance'].diff(periods=48).values[-1]
#         hourly_diff_pct= (df.iloc[-49:]['Balance'].pct_change(periods=48).values[-1])*100
#         if math.isinf(hourly_diff_pct):
#             hourly_diff_pct = 100
#         if math.isnan(hourly_diff):
#             hourly_diff = 0
#         if math.isnan(diff):
#             diff = 0.00
#         if math.isinf(diff):
#             diff = 100
#         average_daily_difference = round(y.mean(), 5)
#         average_daily_dollar_gainz = round(average_daily_difference * data[token]['Current Price'], 2)
#
#         average_weekly_difference = round(z.mean(), 5)
#         average_weekly_dollar_gainz = round(average_weekly_difference * data[token]['Current Price'], 2)
#
#         average_monthly_difference = round(p.mean(), 5)
#         average_monthly_dollar_gainz = round(average_monthly_difference * data[token]['Current Price'], 2)
#
#         data[token]['Current Value'] = '$' + str(round(df.iloc[-1:]['Value_Dollars'].values[0], 2))
#         data[token]['Daily Increase'] = str(hourly_diff) + ' ' + token
#         data[token]['Average Daily Value Increase'] = '$' + str(hourly_diff * data[token]['Current Price'])
#         data[token]['Daily % Change'] = str(round(hourly_diff_pct, 2)) + '%'


df = pd.read_csv(plotting_path + 'Totals' + '_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
y = df.groupby(pd.Grouper(key='Date', freq='30min'))['Balance'].mean().to_frame()
df['Date'] = df['Date'].dt.strftime('%d/%m')
todays_gain_pct = round(y['Balance'].pct_change(periods = 48).values[-1], 2)*100
todays_gain = round(y.iloc[-49:]['Balance'].diff(periods=48).values[-1], 3)
new_df = y['Balance'].diff().round(2)
new_df = new_df.reset_index()
new_df['Date'].dt.strftime('%d/%m')
new_df.to_csv(plotting_path + 'daily_gains.csv', index=False)