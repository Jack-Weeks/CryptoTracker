import discord
from discord.ext import tasks
import pandas as pd
import json
import asyncio
import csv
import os
import datetime
from analysis import analysis
from CryptoDash.create import make_html
token = 'ODYwOTE5MzIyNzEyOTk3ODg4.YOCPmQ.0ke9SGV3t0ka2V16EsyuXBaprgc'
plotting_path = r"D:\Programming\pythonProject\docs\graphing\data\\"
client = discord.Client()
data = pd.DataFrame(columns=['Content', 'Time'])


@client.event
async def on_ready():
    print('Bot Ready')


@client.event
async def on_message(message):
    msg = await client.get_channel(854713826598191137).history(limit=1).flatten()
    msg = msg[0]
    data = pd.DataFrame(columns=['Content', 'Time'])
    data = data.append({'Content': msg.content,
                        'Time': msg.created_at}, ignore_index=True)

    data.to_csv('Messages.csv', index=False)


# @client.event
# async def announce(message):
#     channel = client.get_channel('868895446154748024')
#     channel.send('Hi')
#     await message.channel.send("Bot's message")


async def find_balance():
    while (True):
        import requests
        from bs4 import BeautifulSoup
        import json
        import pandas as pd
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import coinmarketcapapi
        import time
        with open(r"D:\Programming\pythonProject\addy.json", "r") as file:
            token_dict = json.load(file)
        api_call_list = []
        url = 'https://market.posat.io/'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, parser='xml')
        cards = soup.findAll('div', {'class': 'card'})

        x = requests.get('https://farmr.net/read.php?user=95534481070362624').json()

        def get_sit_data():
            url = 'https://chiaforkscalculator.com/silicoin'
            request = requests.get(url)
            soup = BeautifulSoup(request.text, parser='xml')
            current_price = float(soup.find(text='Silicoin coin tSIT price ').findNext('input')['value'])
            url = 'https://alltheblocks.net/silicoin/address/tsit1jsrene5l6kvmkazpgcynz9x38sfgk2w965re9f6g0rla3ahyptkqpznr54'
            request = requests.get(url)
            soup = BeautifulSoup(request.text, parser='xml')
            current_balance = float(soup.find('table').findNext('td', {'data-label': 'Balance'}).text.split()[1])

            if current_price != 0:
                token_dict['SIT']['Current Price'] = current_price
            if current_balance != 0:
                token_dict['SIT']['Current Balance'] = current_balance

        #
        def get_mass_data():
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            # options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Chrome('./chromedriver', options=options)
            url = 'https://www.massexplorer.org/address/ms1qq0zvnsm7vf43mkvh6p8nuhe7f9r2l923tmtr56enrj97tv8sg0lcqv90zht'
            driver.get(url)
            time.sleep(3)
            try:
                balance = float(driver.find_element_by_xpath(
                    '//*[@id="app"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/span').text.split()[0])
            except:
                print("Couldn't get MASS Balance")
            if balance != 0:
                token_dict['MASS']['Current Balance'] = balance

        def get_weave_data():
            url = 'https://viewblock.io/arweave/address/RzfJuyW51BmAVet9imfhcKBFDMskJcSlNXdPHH9sWHE'
            request = requests.get(url)
            soup = BeautifulSoup(request.text, features="lxml")
            x = soup.find('div', {'class': "ud6aj3-3 gHxoUx"}).findNext().findNext().text
            balance = float(x.split()[0])
            print(balance)

            if balance != 0:
                token_dict['Arweave']['Current Balance'] = balance
        def get_prices():
            cmc_api_key = 'a98e9495-0d8f-438b-8691-cb08d162cd59'
            cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
            for token in ['Chia', 'MASS', 'Arweave']:
                if token == 'Chia':
                    symbol = 'XCH'
                if token == 'MASS':
                    symbol = 'MASS'
                if token == 'Arweave':
                    symbol = 'AR'
                call = cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='USD').data
                token_dict[token]['Current Price'] = round(call[symbol]['quote']['USD']['price'], 2)

        def update_csv(input_csv, symbol, storage_dict):
            df = pd.read_csv(input_csv, header=0, index_col=0)
            if len(df.columns) < 2:
                df = pd.read_csv(input_csv, header=0)
            df_cols = list(df.columns)
            today = pd.to_datetime('now', exact=False)
            new_row = pd.DataFrame(data=[
                [float(storage_dict['Current Balance']), storage_dict['Current Price']]],
                                   columns=df_cols, index=[today])
            output_df = pd.concat([df, new_row], ignore_index=False).reset_index()
            output_df.columns = ['Date', 'Balance', 'Price']
            output_df.to_csv(input_csv, index=False)
            ### Update CSV

        def update_total(input_csv, total):
            df = pd.read_csv(input_csv, header=0, index_col=0)
            df_cols = list(df.columns)
            today = pd.to_datetime('now', exact=False)
            new_row = pd.DataFrame(data=[
                total],
                columns=df_cols, index=[today])
            output_df = pd.concat([df, new_row], ignore_index=False).reset_index()
            output_df.columns = ['Date', 'Balance']
            output_df.to_csv(input_csv, index=False)
            ### Update Json

        #### Load Json with Previous Deets

        for card in cards:
            coin = card.findNext('div').text.strip()
            price = card.findNext('div').findNext('div').text.strip()
            #### Prices ####
            if price != 0:
                try:
                    token_dict[coin]['Current Price'] = float(price)
                except:
                    print('Cannot update price for', coin)
            ## TRY
            for i in x['harvesters']:
                try:
                    if token_dict[coin]["Symbol"] == str((i['data']['crypto'])).upper():
                        if coin in ['Chia', 'Flax', 'SIT']:
                            balance = i['data']['wallets'][2]['collateralBalance'] / 1000000000000 + \
                                      i['data']['wallets'][2]['pendingBalance'] / 1000000000000 \
                                      + i['data']['balance']
                            url = f'https://{coin.lower()}.posat.io/address/{token_dict[coin]["Addy"]}'
                            request = requests.get(url)
                            soup = BeautifulSoup(request.text, parser='xml')
                            balance = balance + float(
                                soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0])
                            EC = i['data']['wallets'][2]['capacity'] / 1000000000000
                            if EC != 0:
                                token_dict[coin]['EC'] = EC
                            if balance != 0:
                                token_dict[coin]['Current Balance'] = balance
                except:
                    pass
            if coin not in ['Chia', 'Flax']:
                try:
                    url = f'https://{coin.lower()}.posat.io/address/{token_dict[coin]["Addy"]}'
                    request = requests.get(url)
                    soup = BeautifulSoup(request.text, parser='xml')
                    try:
                        balance = float(soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0])
                    except:
                        balance = float(
                            soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0].replace(',',
                                                                                                                ''))
                    # previous_balance = data[coin]['Balance']
                    if balance != 0:
                        token_dict[coin]['Current Balance'] = balance
                except:
                    print('Could not get explorer for', coin)
        try:
            get_sit_data()
        except:
            print('Unable to Update SIT')
        try:
            get_mass_data()
        except:
            print('Unable to Update MASS')
        try:
            get_weave_data()
        except:
            print('Unable to get Arweave Data')
        try:
            get_prices()
        except:
            print('Unable to get API Prices')
        with open(r"D:\Programming\pythonProject\addy.json", "w") as outfile:
            json.dump(token_dict, outfile, indent=4)

        out = []
        lol = '\n '
        total = 0
        now = datetime.datetime.now().strftime("%a %d - %b %H:%M")
        names = []
        prices = []
        for key in token_dict.keys():
            if key != 'Total':
                if not os.path.exists(plotting_path + str(token_dict[key]['Symbol']) + '_data.csv'):
                    df = pd.DataFrame(columns=['Balance', 'Price'])
                    df.to_csv(plotting_path + str(token_dict[key]['Symbol']) + '_data.csv', index=False)
                csv_path = plotting_path + str(token_dict[key]['Symbol']) + '_data.csv'
                try:
                    update_csv(csv_path, str(token_dict[key]['Symbol']), token_dict[key])
                except:
                    print(key, 'cannot update CSV')
                print(key)
                try:
                    value = float(token_dict[key]['Current Price']) * float(token_dict[key]['Current Balance'])
                    token_dict[key]['Current Value'] = round(value, 2)
                    total += value
                    print(key, token_dict[key]['Current Value'])
                    names.append(key)
                    prices.append((round(value, 2)))
                except:
                    print(key, 'has no value')
                    names.append(key)
                    prices.append(0)
        # names.append('Total')
        # prices.append(round(total, 2))
        zipped = list(zip(names, prices))
        out = sorted(zipped, key=lambda x: x[1], reverse=True)


        line = f"Total Value : ${round(total, 2)}"
        update_total('D:\Programming\pythonProject\docs\graphing\data\Totals_data.csv', round(total, 2))
        msg = f":rocket: **** DJ's Hourly Update for {now}**** :rocket:\n"
        msg = msg +'\n'.join(map(lambda x: str(x[0]) + ' : $' + str(x[1]), out))
        msg = msg + f'\n{line}'
        analysis()

        await client.wait_until_ready()
        channel = client.get_channel(868895446154748024)
        await channel.send(msg)
        await asyncio.sleep(3600)


client.loop.create_task(find_balance())
client.run(token)
