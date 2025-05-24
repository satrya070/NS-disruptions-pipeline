import boto3
import json

from config import TRACKING_COINS
from etl_util import process_spaces

def extract():
    coins_list_param = [process_spaces(coin) for coin in TRACKING_COINS]  # process coinnames with spaces
    coins_list_param = "%2C".join(coins_list_param)  # build string param with commas

    coins_data = fetch_data(coin_list_params)

def load():
    print("load data into sqlite")

def transform():
    print("perform enhancement aggregations")