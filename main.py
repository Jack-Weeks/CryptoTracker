import time
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import coinmarketcapapi
import pandas as pd
import json
from analysis import analysis
from flask import Flask
from pyvirtualdisplay import Display

app = Flask(__name__)

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
    }
}

api_call_list = []
def farmr_api_call():

    x = requests.get('https://farmr.net/read.php?user=95534481070362624').text
    blocks = x.split(';;')
    for block in blocks:
        try:
            json_dict = json.loads(block)
            api_call_list.append(json_dict[0])
            crypto_name = json_dict[0]['crypto'].upper()
            storage[crypto_name]['Current Balance'] = json_dict[0]['balance']
        except:
            pass




def make_dfs():
    for token in storage.keys():
        if not os.path.exists(str(token) + '_data.csv'):
            df = pd.DataFrame(columns=['Balance', 'Price'])
            df.to_csv(str(token) + '_data.csv', index=False)


def get_prices():
    cmc_api_key = 'a98e9495-0d8f-438b-8691-cb08d162cd59'
    cmc = coinmarketcapapi.CoinMarketCapAPI(cmc_api_key)
    for symbol in storage.keys():
        try:
            data = cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='USD').data
            storage[symbol]['Current Price'] = data[symbol]['quote']['USD']['price']
        except:
            storage[symbol]['Current Price'] = 0


def update_csv(input_csv, symbol, storage_dict=storage):
    df = pd.read_csv(input_csv, header=0, index_col=0)
    if len(df.columns) < 2:
        df = pd.read_csv(input_csv, header=0)
    df_cols = list(df.columns)
    today = pd.to_datetime('now', exact=False).strftime("%d/%m/%Y %I:%M:%S")
    new_row = pd.DataFrame(data=[[storage_dict[symbol]['Current Balance'], storage_dict[symbol]['Current Price']]],
                           columns=df_cols, index=[today])
    output_df = pd.concat([df, new_row], ignore_index=False).reset_index()
    output_df.columns = ['Date', 'Balance', 'Price']
    output_df.to_csv(input_csv, index=False)
    # storage_dict[symbol]['Balance History'] = dict(zip(output_df['Date'], output_df['Balance']))


def get_arweave_data():
    url = 'https://viewblock.io/arweave/address/RzfJuyW51BmAVet9imfhcKBFDMskJcSlNXdPHH9sWHE'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="lxml")
    x = soup.find('div', {'class': "ud6aj3-3 gHxoUx"}).findNext().findNext().text
    balance = float(x.split()[0])
    symbol = x.split()[1]
    storage[symbol]['Current Balance'] = balance

    update_csv('AR_data.csv', symbol)


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
    flax_pool_balance = driver.find_element_by_xpath(
        '/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[3]/div[1]/div/div[2]/span')
    pool_balance = float(flax_pool_balance.text.split()[0])
    symbol = flax_pool_balance.text.split()[1]
    driver.quit()

    storage[symbol]['Current Balance'] = flax_balance + pool_balance

    update_csv('XFX_data.csv', symbol)


def get_chia_data():

    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get('https://chia-og.foxypool.io/my-farmer')
    driver.minimize_window()
    pool_key_input = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/input')
    pool_key_input.send_keys(
        '8cae91ac66fd08959589339242980a88336bbb201c75a38cda84e32f1e4e1db06cbb52e2c7c57242528acab832ace197')
    login_button = driver.find_element_by_xpath('/html/body/app-root/div/app-my-farmer/div/div/div/button')
    login_button.click()
    time.sleep(0.5)
    chia_pool_balance = driver.find_element_by_xpath(
        '/html/body/app-root/div/app-my-farmer/div/div/div/div[1]/div[3]/div[1]/div/div[2]/span')
    pool_balance = float(chia_pool_balance.text.split()[0])
    symbol = chia_pool_balance.text.split()[1]

    driver.get(
        'https://www.chiaexplorer.com/blockchain/address/xch1zxnqwv585mua5u98dhhgadxft7u9lys78vuluwtmmy273r984t9qycrtp6')
    time.sleep(1.5)
    balance = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/span[1]').text
    chia_balance = float(balance.split()[0])
    symbol = balance.split()[1]
    driver.quit()

    storage[symbol]['Current Balance'] = chia_balance + pool_balance

    update_csv('XCH_data.csv', symbol)

def get_spare_data():
    update_csv('Spare_data.csv', 'SPARE')

def get_chaingreen_data():
    update_csv('CGN_data.csv', 'CGN')
def execute():
    farmr_api_call()
    make_dfs()
    get_prices()
    get_arweave_data()
    get_flax_data()
    get_chia_data()
    get_chaingreen_data()
    get_spare_data()


def main():
    execute()
    with open("output.json", "w") as outfile:
        json.dump(storage, outfile, indent=4)

    data = analysis()
    with open ('docs/index.MD', 'w') as f:
        f.write('```yaml\n')
        f.close()
    with open("docs/index.MD", "a") as outfile:
        json.dump(data, outfile, indent=4)
    testing_my_patience = """<html>
    <head>
        <title>Convert JSON Data to HTML Table</title>
        <style>
            th, td, p, input {
                font:14px Verdana;
            }
            table, th, td 
            {
                border: solid 1px #DDD;
                border-collapse: collapse;
                padding: 2px 3px;
                text-align: center;
            }
            th {
                font-weight:bold;
            }
        </style>
    </head>
    <body>
        <input type="button" onclick="CreateTableFromJSON()" value="Create Table From JSON" />
        <p id="showData"></p>
    </body>
    
    <script>
        function CreateTableFromJSON() {
            var myBooks = ["""+str(data)+""""
            ]
    
            // EXTRACT VALUE FOR HTML HEADER. 
            // ('Book ID', 'Book Name', 'Category' and 'Price')
            var col = [];
            for (var i = 0; i < myBooks.length; i++) {
                for (var key in myBooks[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }
    
            // CREATE DYNAMIC TABLE.
            var table = document.createElement("table");
    
            // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
    
            var tr = table.insertRow(-1);                   // TABLE ROW.
    
            for (var i = 0; i < col.length; i++) {
                var th = document.createElement("th");      // TABLE HEADER.
                th.innerHTML = col[i];
                tr.appendChild(th);
            }
    
            // ADD JSON DATA TO THE TABLE AS ROWS.
            for (var i = 0; i < myBooks.length; i++) {
    
                tr = table.insertRow(-1);
    
                for (var j = 0; j < col.length; j++) {
                    var tabCell = tr.insertCell(-1);
                    tabCell.innerHTML = myBooks[i][col[j]];
                }
            }
    
            // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
            var divContainer = document.getElementById("showData");
            divContainer.innerHTML = "";
            divContainer.appendChild(table);
        }
    </script>
    </html>"""
    # with open("index.html", "w") as outfile:
    #     outfile.write(testing_my_patience)
    #     outfile.close()

    with open('docs/index.MD', 'a+') as file:
        file.write("\n```")
        file.close()

    return data

@app.route("/")
def index():
    output = main()
    return output

main()

