from lxml import html
import requests

from bs4 import BeautifulSoup
import urllib



masterCMCURL = 'https://coinmarketcap.com/currencies/'
coinDict = {}
skip_list = ['BCD/ETH']
notWithdrawable = ['eos','bitcoin-gold','qtum']
korean ='Bithumb'  #'Korbit' #'Bithumb' 'Coinone'


for coin in ['ripple','ethereum','bitcoin-cash','litecoin','dash','monero','ethereum-classic','zcash']:
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
            if tds[1].text.strip() == korean:
                print(tds[1].text.strip() + ' : ' + dollar_value)
                coinDict[coin][korean] = {}
                coinDict[coin][korean]['dollar'] = dollar_value
                coinDict[coin][korean]['pair'] = pair
            if coin == 'ethereum':
                if tds[1].text.strip() == 'Bitstamp':
                    if pair == 'ETH/USD':
                        coinDict[coin]['Binance'] = {}
                        coinDict[coin]['Binance']['dollar'] = dollar_value
                        coinDict[coin]['Binance']['pair'] = pair
            else:
                if tds[1].text.strip() == 'Binance':
                    print(tds[1].text.strip() + ' : ' + dollar_value)

                    if 'Binance' in coinDict[coin]:
                        if coin == 'ripple':
                            if float(coinDict[coin]['Binance']['dollar']) > float(dollar_value):
                                coinDict[coin]['Binance']['dollar'] = dollar_value
                                coinDict[coin]['Binance']['pair'] = pair
                        else:
                            if float(coinDict[coin]['Binance']['dollar']) < float(dollar_value):
                                coinDict[coin]['Binance']['dollar'] = dollar_value
                                coinDict[coin]['Binance']['pair'] = pair
                    else:
                        coinDict[coin]['Binance'] = {}
                        coinDict[coin]['Binance']['dollar'] = dollar_value
                        coinDict[coin]['Binance']['pair'] = pair

print(coinDict)
coinRatioDict = {}
for coin in coinDict:
    try:
        ratio = float(coinDict[coin][korean]['dollar'])/float(coinDict[coin]['Binance']['dollar'])
        print(coin + ' : ' + str(ratio) + ' : ' + str(coinDict[coin][korean]['dollar']))
    except:
        ratio = 2

    coinRatioDict[ratio] = coin


print()
print("the values of interest are:")
print()
sortedCoinRatioDict = sorted(coinRatioDict)
for key in sortedCoinRatioDict:
    print ( coinRatioDict[key] + ' : ' + coinDict[coinRatioDict[key]]['Binance']['pair'] + ' : ' + str(key) )

print()
coin = 'ripple'
for numCoins in  [200,1000]:
    gain = float(coinDict[coin][korean]['dollar']) * (1/sortedCoinRatioDict[0]) * numCoins  - numCoins * float(coinDict[coin]['Binance']['dollar'] )
    transactionFees = 0.003 * float(coinDict[coin][korean]['dollar']) * numCoins + 1 + 9
    print('profit for ' + str(numCoins) + 'is : ' + str (gain-transactionFees ) )
