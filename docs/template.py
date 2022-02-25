#%%
from decouple import config
from crypto_price import CryptoDataExtractor
# %%
API_KEY = config("API_KEY")
API_SECRET = config("API_SECRET")
extractor = CryptoDataExtractor()
extractor.from_binance(api_key=API_KEY,api_secret=API_SECRET)
# %%
