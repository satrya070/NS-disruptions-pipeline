import boto3
import sqlite3

from crypto_data.config import TRACKING_COINS
from crypto_data.apis.coingecko_api import CoinGeckoAPI

def extract_data() -> list[tuple]:
    """
    extracts the data from the api and returns a list of insertable tuples
    """
    crypto_api = CoinGeckoAPI()
    coin_api_data = crypto_api.fetch_coins_data(TRACKING_COINS)
    
    return coin_api_data

def load_data(coin_insert_data: dict[str, dict]):
    """
    insert data in sqlite db
    """
    insert_coin_data_query = "INSERT INTO coins_data (name, price, change_24h, volume_24h, market_cap)" \
    "VALUES (?, ?, ?, ?, ?)"

    try:
        with sqlite3.connect("/home/satrya070/Documents/github/crypto-data/data/crypto-db.db") as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_coin_data_query, coin_insert_data)
            conn.commit()
            cursor.close()

    except sqlite3.Error as e:
        raise e

def transform():
    print("perform enhancement aggregations")