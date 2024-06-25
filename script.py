#!/usr/bin/env python3

##################################################################
#
#
#  Stock Monitoring to influxDB
#
#  Python script monitoring stocks
#  from google finance data
#
#  contact@dgidgi.ovh
#  
#  v1 : fist version
#  v2 : switch from yahoo data to google finance
#
##################################################################

import json
import os
import time
import configparser
import requests
from bs4 import BeautifulSoup
from influxdb_client import InfluxDBClient, WriteOptions


# config loading
Config = configparser.ConfigParser()
Config.read('config.ini')
Org=Config.get('influx2', 'org')

# set influxDB connexion
Client = InfluxDBClient.from_config_file("config.ini")

# set google finance var
BaseUrl="https://www.google.com/finance"

with open('stocks.json') as data_file:
    Data = json.load(data_file)
    # loop on each stock
    for action in Data['stocks']:
        # get stock value
        Index=action["index"]
        Symbol=action["symbol"]
        TargetUrl=f"{BaseUrl}/quote/{Symbol}:{Index}"
        # make an HTTP request
        Page = requests.get(TargetUrl)
        # use an HTML parser to grab the content from "page"
        soup = BeautifulSoup(Page.content, "html.parser")
        # get the div class containing the current value
        CurrentValue=soup.find("div", {"class": "YMlKec fxKbKc"}).text.replace('€', '')
        CurrentValue = float(CurrentValue)
        #fill data for influxdb
        JsonBody = [{
            "measurement": "cours",
            "tags": {
                "name": action['name'],
                "symbol": action['symbol'],
                "index" : action["index"]
            },
            "fields": {
                "price": CurrentValue,
                "quantity": action['quantity'],
                "cost": action['spent']
            }
        }]
        # send data to influxdb
        Write_api = Client.write_api(write_options=WriteOptions(flush_interval=300, max_retry_time=100))
        Write_api.write("Stocks", Org, JsonBody)
        print(action["name"])
        time.sleep(5)
