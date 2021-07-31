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
