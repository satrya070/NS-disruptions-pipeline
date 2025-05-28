import psycopg2
import os

from ns_disruptions.config import DISRUPTION_FIELDS
from ns_disruptions.apis.ns_api import nsAPI
from ns_disruptions.ns_util import process_ns_data
from ns_disruptions.data_interfaces.ns_dataclasses import DisruptionData, DisruptionStationLink

class ETL:
    def extract_data(self) -> list[dict]:
        """
        extracts the data from the api and list of raw disruption data
        """
        ns_api = nsAPI()
        ns_api_data = ns_api.fetch_disruption_data()

        return ns_api_data
    
    def transform_data(self, ns_api_data: list[dict]) -> list[tuple]:
        """
        performs all required transformations on the data before database insert
        """
        processed_data = process_ns_data(ns_api_data)
        
        return processed_data

    def load_data(self, processed_data: tuple):
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
