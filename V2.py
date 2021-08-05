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
with open('addy.json', "r") as file:
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
    current_balance = float(soup.find('table').findNext('td', {'data-label':'Balance'}).text.split()[1])

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
        balance = float(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/span').text.split()[0])
    except:
        print("Couldn't get MASS Balance")
    if balance != 0:
        token_dict['MASS']['Current Balance'] = balance

def get_prices():
    cmc_api_key = 'a98e9495-0d8f-438b-8691-cb08d162cd59'
    cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
    for token in ['Chia', 'MASS']:
        if token == 'Chia':
            symbol = 'XCH'
        if token == 'MASS':
            symbol = 'MASS'
        call = cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='USD').data
        token_dict[token]['Current Price'] = round(call[symbol]['quote']['USD']['price'], 2)

    ### Update CSV
    ### Update Json


#### Load Json with Previous Deets


for card in cards:
    coin = card.findNext('div').text.strip()
    price = float(card.findNext('div').findNext('div').text.strip())
#### Prices ####
    if price != 0:
        try:
            token_dict[coin]['Current Price'] = price
        except:
            print('Cannot update price for', coin)
    ## TRY
    for i in x['harvesters']:
        try:
            if token_dict[coin]["Symbol"] == str((i['data']['crypto'])).upper():
                if coin in ['Chia', 'Flax', 'SIT']:
                    balance = i['data']['pendingBalance'] + i['data']['collateralBalance'] + i['data']['walletBalance']
                    url = f'https://{coin.lower()}.posat.io/address/{token_dict[coin]["Addy"]}'
                    request = requests.get(url)
                    soup = BeautifulSoup(request.text, parser='xml')
                    balance = balance + float(soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0])
                    if balance != 0:
                        token_dict[coin]['Current Balance'] = balance
        except:
            pass
    if coin not in ['Chia','Flax']:
        try:
            url = f'https://{coin.lower()}.posat.io/address/{token_dict[coin]["Addy"]}'
            request = requests.get(url)
            soup = BeautifulSoup(request.text, parser='xml')
            try:
                balance = float(soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0])
            except:
                balance = float(soup.find('div', {'class': 'float-end'}).findNext('strong').text.split()[0].replace(',',''))
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
    get_prices()
except:
    print('Unable to get API Prices')
with open("addy.json", "w") as outfile:
    json.dump(token_dict, outfile, indent=4)




###Package Json and Update HTML
