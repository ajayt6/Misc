from lxml import html
import requests

from bs4 import BeautifulSoup
import urllib



masterCMCURL = 'https://coinmarketcap.com/currencies/'
coinDict = {}
skip_list = ['BCD/ETH']
notWithdrawable = ['eos','bitcoin-gold','qtum']
indian ='Koinex'  #'Korbit' #'Bithumb' 'Coinone'
american = 'Bitstamp'

for coin in ['ripple']:
    print()
    print()
    print(coin)
    coinDict[coin] = {}
    tempURL = masterCMCURL + coin + '#markets'

    req = urllib.request.Request(
        tempURL,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    html = urllib.request.urlopen(req)

    #html = urlopen(tempURL)
    soup = BeautifulSoup(html, 'html.parser')

    # Take out the <div> of name and get its value
    name_box = soup.find('div', attrs = {'class':'table-responsive'})
    table_rows =  name_box.find('table', attrs = {'id':'markets-table'}).find_all('tr')
    for row in table_rows:
        tds = row.find_all('td')
        if len(tds) >= 5:
            dollar_value = tds[4].text.strip()[1:]
            dollar_value = "".join(dollar_value.split()).replace('$','')
            pair = tds[2].text.strip()
            if pair in skip_list:
                continue
            if tds[1].text.strip() == indian:
                print(tds[1].text.strip() + ' : ' + dollar_value)
                coinDict[coin][indian] = {}
                coinDict[coin][indian]['dollar'] = dollar_value
                coinDict[coin][indian]['pair'] = pair
            else:
                if tds[1].text.strip() == american and pair == 'XRP/USD':
                    print(tds[1].text.strip() + ' : ' + dollar_value)

                    coinDict[coin][american] = {}
                    coinDict[coin][american]['dollar'] = dollar_value
                    coinDict[coin][american]['pair'] = pair

print(coinDict)
coin = 'ripple'
indianPrice = float(coinDict[coin][indian]['dollar'])
americanPrice = float(coinDict[coin][american]['dollar'])
priceDiff =  indianPrice- americanPrice

numCoins=1000

gst = 2.3/100 * numCoins * indianPrice
cardCharge = 5.0/100 * numCoins * americanPrice
profit = numCoins * priceDiff - gst - cardCharge

print("gst is: " + str(gst))
print("card charge is: " + str(cardCharge))
print("The total profit is: " + str(profit))