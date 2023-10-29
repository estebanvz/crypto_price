import os
import sys
import time
from datetime import datetime, timedelta
from google.cloud import storage
import io
import numpy as np
# import pandas as pd
# import plotly.graph_objs as go
# import plotly.offline as py
from binance.client import Client
from binance.enums import HistoricalKlinesType

BINANCE_API = "https://api.binance.com/api"
def save_numpy_array_to_gcs(bucket_name, file_name, numpy_array):
    # Convert NumPy array to bytes
    with io.BytesIO() as output:
        np.save(output, numpy_array)
        output.seek(0)
        data = output.read()
    # Authenticate and create a client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Create a blob (file) in the bucket and upload the NumPy array data
    blob = bucket.blob(file_name)
    blob.upload_from_string(data)

    print(f"NumPy array saved to {bucket_name}/{file_name} in Google Cloud Storage")

class CryptoDataExtractor:
    def __init__(self, save_path, criptos=["BTCUSDT"], gcp = True) -> None:
        self.save_path = save_path
        self.gcp = gcp
        self.criptos = criptos
        if(self.gcp is False):
            if(os.path.isdir(self.save_path) is False):
                os.mkdir(self.save_path)

    def from_binance(
        self, api_key="", api_secret="", time_in_hours=24, time_interval="1h"
    ):
        if(self.gcp is False):
            time_folder = "{}/{}".format(self.save_path, time_interval)   
            if(os.path.isdir(time_folder) is False):
                os.mkdir(time_folder)
        client = Client(api_key, api_secret)
        client.API_URL = BINANCE_API

        timestamp = datetime.utcnow() - timedelta(hours=time_in_hours)
        unixtime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        bucketTime = timestamp.strftime("%Y%m%d%H%M%S")
        for cripto in self.criptos:
            bars = client.get_historical_klines(cripto, time_interval, unixtime)
            if len(bars) >= 60:
                if(self.gcp):
                    save_numpy_array_to_gcs(self.save_path,f"{bucketTime}-{cripto}",bars)
                else:
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