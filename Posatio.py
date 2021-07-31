import requests
from bs4 import BeautifulSoup

forks = {}
url = 'https://market.posat.io/'
request = requests.get(url)
soup = BeautifulSoup(request.text, parser='xml')
cards = soup.findAll('div', {'class': 'card'})

#### Load Json with Previous Deets


for card in cards:
    coin = card.findNext('div').text.strip()
    price = card.findNext('div').findNext('div').text.strip()
    forks[coin] = {'Current Price': price}
    ## TRY

        ### Use coin name to Build new Posat URL


        ### IF Balance is non zero and Different to previous value update value
    ### Except Leave values as is
    ### Try
    ### Get Selenium Data
    ### Add Values from Selenium if they work

    ### Update CSV
    ### Update Json

