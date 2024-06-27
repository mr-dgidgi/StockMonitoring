# StockMonitoring
Python script to create stocks time series in influxdb
It simply ceate en entry with the last price, the number of stocks and the price spent to buy the current stocks
This script has been made to work with influxdb 2.x so if you whant to use 1.8 you will have to change some things on the script.

To create this script I was inspired by these 2 articles : 

https://www.scrapingdog.com/blog/scrape-google-finance/
https://pbrissaud.github.io/suivi-bourse/

## config.ini
just the basic data to setum the connexion to the influxdb

## stocks.json
The must important part for the basic user

| variable                      | meaning                                                |
|-------------------------------|--------------------------------------------------------|
| name                          | a common name for the stock                            |
| index                         | the place where the stock is sale (NDAQ, FRA, EPA ...) |
| symbol                        | the common symbol of the stock                         |
| portfolio[]                   | table containing owned stocks info                     |
| portfolio.datebought          | date when the stock has been bought                    |
| portfolio.datesell            | date when the stock has been sold                      |
| portfolio.quantity            | the number of stock that you have                      |
| portfolio.price               | money spent to buy the stocks                          |
| portfolio.pricesell           | selling price of the stock                             |


### Exemple : 

in this exemple whe have 0.5 stock from IT6 sold on Frankfurt (FRA) brought at 50€ and 10 stock of NVIDIA sold on NASDAQ brought at 1000€

        "stocks": [
                {
                        "name": "Itron",
                        "index": "FRA",
                        "symbol": "IT6",
                        "portfolio": [
				{	
					"datebought":"2024-06-17",
     					"datesell":"",
					"quantity": 0.5,
					"price": 50.00,
					"pricesell": 0
				}
                            ]
                },
                {
                        "name": "NVIDIA",
                        "index": "NDAQ",
                        "symbol": "NVDA",
                        "portfolio": [
				{	
					"datebought":"2024-06-17",
     					"datesell":"",
					"quantity": 10,
					"price": 1000.00,
					"pricesell": 0
				}
                            ]
                }
If you don't know what is the index and the symbol go to google finance and check the url of the stock that you want. ex : [https://www.google.com/finance/quote/**IT6**:**FRA**](https://www.google.com/finance/quote/IT6:FRA)

If you don't like/use the quantity or spent value you can remove it but think to remove it also on the script. Il you want to add somme value, do waht you whant, just copy what I've already done on the script also. You're a big boy.

## script.py 
The script is setup to use python in virtual env located in /home/python/. So if it is not working modify the shebang or create a virtualenv
For the script you also need some packages from pip (so install pip before ;) )

    pip3 install configparser
    pip3 install influxdb-client
    pip3 install beautifulsoup4
    pip3 install requests

## cron.d/StockMonitoring

If you don't know what to do with that file I think you shouldn't try to use this project.
