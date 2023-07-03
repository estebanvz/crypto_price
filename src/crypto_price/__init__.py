import os
import sys
import time
from datetime import datetime, timedelta

import numpy as np
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.offline as py
from binance.client import Client
from binance.enums import HistoricalKlinesType

BINANCE_API = "https://api.binance.com/api"

class CryptoDataExtractor:
    def __init__(self, save_path="./datasets", criptos=["BTCUSDT"]) -> None:
        self.save_path = save_path
        self.criptos = criptos
        if(os.path.isdir(self.save_path) is False):
            os.mkdir(self.save_path)

    def from_binance(
        self, api_key="", api_secret="", time_in_hours=24, time_interval="1h"
    ):
        time_folder = "{}/{}".format(self.save_path, time_interval)   
        if(os.path.isdir(time_folder) is False):
            os.mkdir(time_folder)
        client = Client(api_key, api_secret)
        client.API_URL = BINANCE_API

        timestamp = datetime.utcnow() - timedelta(hours=time_in_hours)
        unixtime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        for cripto in self.criptos:
            bars = client.get_historical_klines(cripto, time_interval, unixtime)
            if len(bars) >= 60:
                np.savetxt(
                    "{}/{}.csv".format(time_folder, cripto),
                    bars,
                    delimiter="|",
                    fmt="%s",
                )
    def get_cryptos():
        client = Client("", "")
        exchange_info = client.get_exchange_info()
        cryptos = [e["symbol"] for e in exchange_info["symbols"] if e["symbol"].endswith('USDT') and 'MARGIN' in e["permissions"]]
        return cryptos