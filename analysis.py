def analysis():
    import pandas as pd
    import json
    import yfinance as yf

    with open('output.json', "r") as file:
        data = json.load(file)
    for token in data.keys():
        try:
            USD_GBP = yf.download('GBPUSD=X', period='1d', interval='1h')
            exchange = USD_GBP['Close'][-1]
            df = pd.read_csv(token + '_data.csv')
            df['Date'] = pd.to_datetime(df['Date'])
            df['% Change in Balance'] = (df.Balance.pct_change(periods=12)) * 100
            df['Balance Diff'] = df.Balance.diff()
            df['Value $ '] = df['Balance'] * data[token]['Current Price']
            df['Value £ '] = df['Value $ '] * exchange
            df['Change in Value'] = df['Balance Diff'] * df['Price']


            x = df.groupby(pd.Grouper(key = 'Date', freq='1h'))['Balance Diff'].mean()
            y = df.groupby(pd.Grouper(key = 'Date', freq='1D'))['Balance Diff'].mean()
            z = df.groupby(pd.Grouper(key = 'Date', freq='1W'))['Balance Diff'].mean()
            p = df.groupby(pd.Grouper(key = 'Date', freq='1M'))['Balance Diff'].mean()

            average_hourly_difference = round(x.mean(), 5)
            average_hourly_dollar_gainz = round(average_hourly_difference * data[token]['Current Price'], 2)

            average_daily_difference = round(y.mean(), 5)
            average_daily_dollar_gainz = round(average_daily_difference * data[token]['Current Price'], 2)

            average_weekly_difference = round(z.mean(), 5)
            average_weekly_dollar_gainz = round(average_weekly_difference * data[token]['Current Price'], 2)

            average_monthly_difference = round(p.mean(), 5)
            average_monthly_dollar_gainz = round(average_monthly_difference * data[token]['Current Price'], 2)

            data[token]['Average Hourly Increase'] = average_hourly_difference
            data[token]['AverageHourly Value Increase'] = average_hourly_dollar_gainz

            data[token]['Average Daily Increase'] = average_daily_difference
            data[token]['Average Daily Value Increase'] = average_daily_dollar_gainz

            # data[token]['Average_Weekly_Increase'] = average_weekly_difference
            # data[token]['Average_Weekly_Value_Increase'] = average_weekly_dollar_gainz
            #
            # data[token]['Average_Monthly_Increase'] = average_monthly_difference
            # data[token]['Average_Monthly_Value_Increase'] = average_monthly_dollar_gainz

            df.to_excel(token + '_analysis.xls', index=False)
        except:
            pass


    total = 0
    for i in data.keys():
        try:
            price = data[i]['Current Price']
            quantity = data[i]['Current Balance']
            total += price * quantity
        except:
            pass
    data['Totals'] = {'Total': total}
    with open("output.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    return data



