import psycopg2
import os

from dataclasses import astuple
from ns_disruptions.apis.ns_api import nsAPI
from ns_disruptions.ns_util import process_ns_data
from ns_disruptions.data_interfaces.ns_dataclasses import DisruptionData, DisruptionStationLink

class ETL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ["PGHOST"],
            port=os.environ["PGPORT"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            dbname=os.environ["PGDATABASE"]
        )

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

    def load_data(self, processed_data: list[tuple]):
        """
        inserts the data into the database
        """
        disruption_insert_data = []
        disrupted_stations_insert_data = []
    
        for disruption, disrupted_stations in processed_data:
            disruption_insert_data.append(astuple(disruption))

            disrupted_stations = [astuple(disrupted_station) for disrupted_station in disrupted_stations]
            disrupted_stations_insert_data = disrupted_stations_insert_data + disrupted_stations

        insert_disruption_query = "INSERT INTO ns.ns_disruptions (id, type, impact, fetch_timestamp) " \
        "VALUES (%s, %s, %s, %s)"

        insert_disruption_station_link_query = "INSERT INTO ns.ns_disruption_station_link (disruption_id, station_code, level, fetch_timestamp) " \
        "VALUES (%s, %s, %s, %s)"

        try:
            cursor = self.conn.cursor()
            cursor.executemany(insert_disruption_query, disruption_insert_data)
            cursor.executemany(insert_disruption_station_link_query, disrupted_stations_insert_data)
            self.conn.commit()

            print("Data inserted succesfully")
            
        except Exception as e:
            print("Data insert failed: ", e)
            self.conn.rollback()
            self.conn.close()
            raise e

        finally:
            cursor.close()

    def refresh_data_views(self):
        """
        refreshed the materialized views to take in the latest data from tables
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("REFRESH MATERIALIZED VIEW ns.disruptions_24h;")
            cursor.execute("REFRESH MATERIALIZED VIEW ns.affected_stations_24h;")
            cursor.execute("REFRESH MATERIALIZED VIEW ns.day_aggregations;")
            cursor.execute("REFRESH MATERIALIZED VIEW ns.map_data;")

            self.conn.commit()

            print("Data refreshed succesfully")
            
        except Exception as e:
            print("Data insert failed: ", e)
            self.conn.rollback()

        finally:
            cursor.close()
            self.conn.close()  # this assumes this function is called as the last data process