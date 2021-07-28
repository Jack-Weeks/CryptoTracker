import time
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import coinmarketcapapi
import pandas as pd
import json
from analysis import analysis
from CryptoDash.create import make_html
from data_cleanup import data_cleanup

plotting_path = 'docs/graphing/data/'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
storage = {
    'XCH': {
        'Current Price': float(),
        'Current Balance': float(),
    },

    'XFX': {
        'Current Price': float(),
        'Current Balance': float(),
    },

    'CGN': {
        'Current Price': float(),
        'Current Balance': float(),
    },

    'SPARE': {
        'Current Price': float(),
        'Current Balance': float(),
    },

    'AR': {
        'Current Price': float(),
        'Current Balance': float(),
    },
    'SIT': {
        'Current Price': float(),
        'Current Balance': float(),

    },
    'XGJ': {
        'Current Price': float(),
        'Current Balance':float(),
    },
    'XFL': {
        'Current Price': float(),
        'Current Balance': float()
    },
    'HDD':{
        'Current Price' : float(),
        'Current Balance' : float()
    },
    'AVO' : {
        'Current Price' : float(),
        'Current Balance': float(),
    },
    'XDG' : {
        'Current Price' : float(),
        'Current Balance' : float(),
    },

    'Totals': {
    }
}
with open('D:\Programming\pythonProject\Altcoin.json', 'r') as altcoin:
    alt_prices = json.load(altcoin)
api_call_list = []


def farmr_api_call():
    x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
    blocks = x.split(';;')
    for block in blocks[:-1]:

        json_dict = json.loads(block)
        api_call_list.append(json_dict[0])
        crypto_name = json_dict[0]['crypto'].upper()
        try:
            storage[crypto_name]['Current Price'] = alt_prices[crypto_name]
        except:
            pass

        if crypto_name == 'SIT':
            storage[crypto_name]['Current Balance'] = str(round(json_dict[0]['walletBalance'], 5)) + ' ' + crypto_name
        else:
            storage[crypto_name]['Current Balance'] = str(round(json_dict[0]['balance'], 5)) + ' ' + crypto_name


def make_dfs():
    for token in storage.keys():
        if not os.path.exists(plotting_path + str(token) + '_data.csv'):
            df = pd.DataFrame(columns=['Balance', 'Price'])
            df.to_csv(plotting_path + str(token) + '_data.csv', index=False)


def get_prices():
    cmc_api_key = 'a98e9495-0d8f-438b-8691-cb08d162cd59'
    cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
    for symbol in storage.keys():
        try:
            if symbol != 'XFL':
                data = cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='USD').data
                storage[symbol]['Current Price'] = round(data[symbol]['quote']['USD']['price'], 2)
                change = round(data[symbol]['quote']['USD']['percent_change_24h'], 2)
                storage[symbol]['24hr Price Change %'] = str(change) + '%'
        except:
            pass


def update_csv(input_csv, symbol, storage_dict=storage):
    df = pd.read_csv(input_csv, header=0, index_col=0)
    if len(df.columns) < 2:
        df = pd.read_csv(input_csv, header=0)
    df_cols = list(df.columns)
    today = pd.to_datetime('now', exact=False)
    new_row = pd.DataFrame(data=[[float(storage_dict[symbol]['Current Balance'].split()[0]), storage_dict[symbol]['Current Price']]],
                           columns=df_cols, index=[today])
    output_df = pd.concat([df, new_row], ignore_index=False).reset_index()
    output_df.columns = ['Date', 'Balance', 'Price']
    output_df.to_csv(input_csv, index=False)
    # storage_dict[symbol]['Balance History'] = dict(zip(output_df['Date'], output_df['Balance']))


def update_totals(input_csv=plotting_path + 'Totals_data.csv', symbol='Totals', storage_dict=storage):
    df = pd.read_csv(input_csv, header=0, index_col=0)
    if len(df.columns) < 1:
        df = pd.read_csv(input_csv, header=0)
    df_cols = list(df.columns)
    today = pd.to_datetime('now', exact=False)
    new_row = pd.DataFrame(data=[[storage_dict[symbol]['Total']]],
                           columns=df_cols, index=[today])
    output_df = pd.concat([df, new_row], ignore_index=False).reset_index()
    output_df.columns = ['Date', 'Balance']
    output_df.to_csv(input_csv, index=False)

    output_df['Date'] = pd.to_datetime(output_df['Date']).dt.strftime('%d/%m')
    output_df.to_csv('docs/graphing/data/Total_analysis.csv', index=False)


def get_arweave_data():
    url = 'https://viewblock.io/arweave/address/RzfJuyW51BmAVet9imfhcKBFDMskJcSlNXdPHH9sWHE'

    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="lxml")
    x = soup.find('div', {'class': "ud6aj3-3 gHxoUx"}).findNext().findNext().text
    balance = float(x.split()[0])
    symbol = x.split()[1]

    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get('https://ar.virdpool.com/#/address/RzfJuyW51BmAVet9imfhcKBFDMskJcSlNXdPHH9sWHE')
    driver.minimize_window()
    time.sleep(2)
    hashrate = driver.find_element_by_xpath('//*[@id="mount_point"]/div/div[2]/table[2]/tbody/tr[2]/td/span').text
    pending_balance = driver.find_element_by_xpath(
        '//*[@id="mount_point"]/div/div[2]/table[4]/tbody/tr[2]/td/span').text
    storage[symbol]['Hashrate'] = hashrate
    driver.close()

    storage[symbol]['Current Balance'] = str(round(balance + float(pending_balance), 5)) + ' AR'
    update_csv(plotting_path + 'AR_data.csv', symbol)


def get_flax_data():
    flax_url = 'https://flaxexplorer.org/blockchain/address/xfx1jsrene5l6kvmkazpgcynz9x38sfgk2w965re9f6g0rla3ahyptkqpsppsn'
    request = requests.get(flax_url)
    soup = BeautifulSoup(request.text, features='lxml')
    flax_balance = float(soup.find('span', {'class': 'stats-value'}).text.split()[0])

    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get('https://flax-og.foxypool.io/my-farmer')
    driver.minimize_window()
    pool_key_input = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/input')
    pool_key_input.send_keys(
        '8cae91ac66fd08959589339242980a88336bbb201c75a38cda84e32f1e4e1db06cbb52e2c7c57242528acab832ace197')
    login_button = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/button')
    login_button.click()
    time.sleep(2)
    pending_balance = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[1]/div[1]/div/div[2]/span').text
    EC = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[1]/div[3]/div/div[2]').text
    flax_pool_balance = driver.find_element_by_xpath(
        '/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[3]/div[1]/div/div[2]/span')
    pool_balance = float(flax_pool_balance.text.split()[0])
    pending_balance = float(pending_balance.split()[0])
    symbol = flax_pool_balance.text.split()[1]
    driver.quit()

    storage[symbol]['Current Balance'] = str(round(flax_balance + pool_balance + pending_balance, 5)) +' XFX'
    storage[symbol]['Wallet Balance'] = str(round(flax_balance, 5)) + ' XFX'
    storage[symbol]['Collateral Balance'] = str(round(pool_balance, 5)) + ' XFX'
    storage[symbol]['Estimated Capacity'] = EC[:9]
    storage[symbol]['Pending Balance'] = str(round(pending_balance, 5)) + ' XFX'

    update_csv(plotting_path + 'XFX_data.csv', symbol)


def get_chia_data():
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get('https://chia-og.foxypool.io/my-farmer')
    driver.minimize_window()
    pool_key_input = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/input')
    pool_key_input.send_keys(
        '8cae91ac66fd08959589339242980a88336bbb201c75a38cda84e32f1e4e1db06cbb52e2c7c57242528acab832ace197')
    login_button = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/button')
    login_button.click()
    time.sleep(10)
    EC = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[1]/div[3]/div/div[2]').text
    pending_balance = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[1]/div[1]/div/div[2]/span').text
    chia_pool_balance = driver.find_element_by_xpath(
        '/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[3]/div[1]/div/div[2]/span')
    pool_balance = float(chia_pool_balance.text.split()[0])
    pending_balance = float(pending_balance.split()[0])
    symbol = chia_pool_balance.text.split()[1]

    driver.get(
        'https://www.chiaexplorer.com/blockchain/address/xch1zxnqwv585mua5u98dhhgadxft7u9lys78vuluwtmmy273r984t9qycrtp6')
    time.sleep(30)
    balance = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/span[1]').text
    time.sleep(60)
    chia_balance = float(balance.split()[0])
    symbol = balance.split()[1]
    driver.quit()

    storage[symbol]['Current Balance'] = str(round(chia_balance + pool_balance + pending_balance, 5)) + ' XCH'
    storage[symbol]['Wallet Balance'] = str(round(chia_balance, 5)) + ' XCH'
    storage[symbol]['Collateral Balance'] = str(round(pool_balance, 5)) + ' XCH'
    storage[symbol]['Estimated Capacity'] = EC[:9]
    storage[symbol]['Pending Balance'] = str(round(pending_balance, 5)) + ' XCH'


    update_csv(plotting_path + 'XCH_data.csv', symbol)


def get_spare_data():
    update_csv(plotting_path + 'SPARE_data.csv', 'SPARE')


def get_chaingreen_data():
    update_csv(plotting_path + 'CGN_data.csv', 'CGN')


def get_sit_data():
    update_csv(plotting_path + 'SIT_data.csv', 'SIT')

def get_xgj_data():
    update_csv(plotting_path + 'XGJ_data.csv', 'XGJ')

def get_xfl_data():
    update_csv(plotting_path + 'XFL_data.csv', 'XFL')

def get_hdd_data():
    update_csv(plotting_path + 'HDD_data.csv', 'HDD')

def get_AVO_data():
    update_csv(plotting_path + 'AVO_data.csv', 'AVO')

def get_XDG_data():
    update_csv(plotting_path + 'XDG_data.csv', 'XDG')
def execute():

    farmr_api_call()
    make_dfs()
    get_prices()
    get_arweave_data()
    get_flax_data()
    get_chia_data()
    get_chaingreen_data()
    get_spare_data()
    get_sit_data()
    get_xgj_data()
    get_xfl_data()
    get_hdd_data()
    get_AVO_data()
    get_XDG_data()
def num_items(d):
    if isinstance(d, list):
        for i in d:
            for ii in num_items(i):
                yield ii
    elif isinstance(d, dict):
        for k, v in d.items():
            for ii in num_items(v):
                yield ii
    else:
        yield 1


def main():
    execute()
    with open("output.json", "w") as outfile:
        json.dump(storage, outfile, indent=4)
    data_cleanup()
    data = analysis()
    update_totals(storage_dict=data)
    with open('README.md', 'w') as f:
        f.write('```yaml\n')
        f.close()
    with open("README.md", "a") as outfile:
        json.dump(data, outfile, indent=4)
    with open('output.json', 'r') as outy:
        make_html(json.load(outy), 'docs/index.html')

    return data


# @app.route("/")
# def index():
#     return render_template('index.html')
#
#
while True:

    main()
    time.sleep(1400)
