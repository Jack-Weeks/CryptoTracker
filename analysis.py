def analysis():
    import pandas as pd
    import json
    import yfinance as yf
    import math
    todays_gain = 0
    todays_gain_pct = 0
    plotting_path = 'docs/graphing/data/'
    with open('output.json', "r") as file:
        data = json.load(file)
    for token in data.keys():
        try:
            USD_GBP = yf.download('GBPUSD=X', period='1d', interval='1h')
            exchange = USD_GBP['Close'][-1]
            df = pd.read_csv(plotting_path + token + '_data.csv')
            df['Date'] = pd.to_datetime(df['Date'])
            df['% Change_in_Balance'] = (df.Balance.pct_change(periods=12)) * 100
            df['Balance_Diff'] = df.Balance.diff()
            df['Value_Dollars'] = df['Balance'] * data[token]['Current Price']
            df['Value_Pounds'] = df['Value_Dollars'] / exchange
            df['Change_in_Value'] = df['Balance_Diff'] * df['Price']

            x = df.groupby(pd.Grouper(key = 'Date', freq='1h'))['Balance_Diff'].sum()
            y = df.groupby(pd.Grouper(key = 'Date', freq='1D'))['Balance_Diff'].sum()
            z = df.groupby(pd.Grouper(key = 'Date', freq='1W'))['Balance_Diff'].sum()
            p = df.groupby(pd.Grouper(key = 'Date', freq='1M'))['Balance_Diff'].sum()
            grouped_daily = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()



            average_hourly_difference = round(x.mean(), 5)
            diff = (grouped_daily['Balance'].pct_change().values[-1] * 100)
            hourly_diff = df.iloc[-49:]['Balance'].diff(periods=48).values[-1]
            hourly_diff_pct = (df.iloc[-49:]['Balance'].pct_change(periods=48).values[-1]) * 100
            if math.isinf(hourly_diff_pct):
                hourly_diff_pct = 100
            if math.isnan(hourly_diff):
                hourly_diff = 0
            if math.isnan(diff):
                diff = 0.00
            if math.isinf(diff):
                diff = 100
            average_daily_difference = round(y.mean(), 5)
            average_daily_dollar_gainz = round(average_daily_difference * data[token]['Current Price'], 2)

            average_weekly_difference = round(z.mean(), 5)
            average_weekly_dollar_gainz = round(average_weekly_difference * data[token]['Current Price'], 2)

            average_monthly_difference = round(p.mean(), 5)
            average_monthly_dollar_gainz = round(average_monthly_difference * data[token]['Current Price'], 2)

            # data[token]['Average Hourly Increase'] = average_hourly_difference
            # data[token]['Average Hourly Value Increase'] = average_hourly_dollar_gainz
            data[token]['Current Value'] = '$' + str(round(df.iloc[-1:]['Value_Dollars'].values[0], 2))
            data[token]['Daily Increase'] = str(round(hourly_diff, 5)) + ' ' + token
            data[token]['Average Daily Value Increase'] = '$' + str(hourly_diff * data[token]['Current Price'])
            data[token]['Daily % Change'] = str(round(hourly_diff_pct, 2)) + '%'

            # data[token]['Average_Weekly_Increase'] = average_weekly_difference
            # data[token]['Average_Weekly_Value_Increase'] = average_weekly_dollar_gainz
            #
            # data[token]['Average_Monthly_Increase'] = average_monthly_difference
            # data[token]['Average_Monthly_Value_Increase'] = average_monthly_dollar_gainz
            df['Date'] = df['Date'].dt.strftime('%d/%m')
            df.to_csv(plotting_path + token + '_analysis.csv', index=False)
            df.to_excel(token + '_analysis.xls', index=False)
        except:
            try:
                df = pd.read_csv(plotting_path + token + '_data.csv')
                df['Date'] = pd.to_datetime(df['Date'])
                y = df.groupby(pd.Grouper(key='Date', freq='1D'))['Balance'].mean().to_frame()
                df['Date'] = df['Date'].dt.strftime('%d/%m')
                todays_gain_pct = round(y['Balance'].pct_change().values[-1], 2)*100
                todays_gain = round(y.iloc[-2:]['Balance'].diff().values[1], 3)
                new_df = y['Balance'].diff().round(2)
                new_df = new_df.reset_index()
                new_df['Date'].dt.strftime('%d/%m')
                new_df.to_csv(plotting_path + 'daily_gains.csv', index=False)

            except:
                print('ya dingus')



    df = pd.read_csv('docs/graphing/data/Totals_data.csv')




    total = 0
    for i in data.keys():
        try:
            price = data[i]['Current Price']
            quantity = float(data[i]['Current Balance'][:-len(i)].strip())
            total += price * quantity
        except:
            pass
    data['Totals'] = {'Total': round(total, 2),
                      "Today's Gain $": todays_gain,
                      "Today's % Gain": todays_gain_pct}
    print(total, todays_gain)
    with open("output.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    return data



