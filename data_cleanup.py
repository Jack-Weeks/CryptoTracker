import pandas as pd
def data_cleanup():
    names = ['AR_data.csv', 'CGN_data.csv', 'SIT_data.csv', 'SPARE_data.csv', 'XCH_data.csv', 'XFX_data.csv']
    path = 'docs/graphing/data/'
    for name in names:
        df = pd.read_csv(path + name, index_col=False)
        df['Date'] = pd.to_datetime(df['Date'])
        grouped = df.groupby(pd.Grouper(key='Date', freq= '30min')).mean()
        grouped2 = grouped['Balance'].interpolate(method='linear')
        grouped['Balance'] = grouped2.values
        grouped2 = grouped['Price'].interpolate(method='linear')
        grouped['Price'] = grouped2.values
        grouped = grouped.reset_index()
        grouped.to_csv(path + name, index=False)

    df = pd.read_csv(path + 'Totals_data.csv', index_col=False)
    df['Date'] = pd.to_datetime(df['Date'])
    grouped = df.groupby(pd.Grouper(key='Date', freq= '30min')).mean()
    grouped2 = grouped['Balance'].interpolate(method='linear')
    grouped['Balance'] = grouped2.values
    grouped = grouped.reset_index()
    grouped.to_csv(path + 'Totals_data.csv', index=False)