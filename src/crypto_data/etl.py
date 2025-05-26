import psycopg2
import os

from crypto_data.config import TRACKING_COINS
from crypto_data.apis.coingecko_api import CoinGeckoAPI


def extract_data() -> list[tuple]:
    """
    extracts the data from the api and returns a list of insertable tuples
    """
    crypto_api = CoinGeckoAPI()
    coin_api_data = crypto_api.fetch_coins_data(TRACKING_COINS)
    
    return coin_api_data


def load_data(coin_insert_tuple_data: list[tuple]):
    """
    inserts the data into the database
    """
    insert_coins_data_query = "INSERT INTO coins_data (name, price, change_24h, volume_24h, market_cap) " \
    "VALUES (%s, %s, %s, %s, %s)"

    try:
        conn = psycopg2.connect(
            host=os.environ["PGHOST"],
            port=os.environ["PGPORT"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            dbname=os.environ["PGDATABASE"]
        )

        cursor = conn.cursor()
        cursor.executemany(insert_coins_data_query, coin_insert_tuple_data)
        conn.commit()

        print("Data inserted succesfully")
        
    except Exception as e:
        print("Data insert failed: ", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def transform_data():
    """
    performs any transformations on the data if needed
    """
    pass