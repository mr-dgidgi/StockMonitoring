#!/usr/bin/env python3

###########################################
#
#
#  Stock Monitoring to influxDB
#
#  From Suivibourse base project
#  https://pbrissaud.github.io/suivi-bourse/
#
#  contact@dgidgi.ovh
#  
#  v1 : fist version
#
###########################################


import json
import os
import time
import configparser
import yfinance as yf
from influxdb_client import InfluxDBClient, WriteOptions


# config loading
config = configparser.ConfigParser()
config.read('config.ini')
org=config.get('influx2', 'org')
# set influxDB connexion
Client = InfluxDBClient.from_config_file("config.ini")
with open('stocks.json') as data_file:
    data = json.load(data_file)
    # loop on each stock
    for action in data['stocks']:
        # get stock value
        ticker = yf.Ticker(action['sigle'])
        history = ticker.history()
        last_quote = (history.tail(1)['Close'].iloc[0])
        #fill data for influxdb
        json_body = [{
            "measurement": "cours",
            "tags": {
                "name": action['name'],
                "sigle": action['sigle']
            },
            "fields": {
                "price": last_quote,
                "quantity": action['quantity'],
                "cost": action['spent']
            }
        }]
        # send data to influxdb
        write_api = Client.write_api(write_options=WriteOptions(flush_interval=300, max_retry_time=100))
        write_api.write("Stocks", org, json_body)
        print(action["name"])
        time.sleep(5)

