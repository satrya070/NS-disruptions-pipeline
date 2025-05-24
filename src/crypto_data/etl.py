import boto3

from crypto_data.config import TRACKING_COINS
from crypto_data.apis.coingecko_api import CoinGeckoAPI

def extract_data() -> list[tuple]:
    """
    extracts the data from the api and returns a list of insertable tuples
    """
    crypto_api = CoinGeckoAPI()
    coin_api_data = crypto_api.fetch_coins_data(TRACKING_COINS)
    
    return coin_api_data

def load_data(coin_api_data: dict[str, dict]):
    

    insert_coin_data_query = "INSERT INTO coins_data (name, price, change_24h, volume_24h, market_cap)" \
    "VALUES (?, ?, ?, ?, ?)"



def transform():
    print("perform enhancement aggregations")