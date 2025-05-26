import requests
import os
import json

from dotenv import load_dotenv
from crypto_data.interfaces.crypto_api import CryptoAPI

load_dotenv()

class CoinGeckoAPI(CryptoAPI):
    def __init__(self):
        self.api_key = os.getenv("COINGECKO_API_KEY")

    def fetch_coins_data(self, coins_list: list[str]) -> dict[str, dict]:
        """coins_list_param = self._prepare_coint_list_param(coins_list)
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=eur&names={coins_list_param}&include_24hr_vol=true&include_24hr_change=true&precision=3&include_market_cap=true"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            raise e  # stop execution
        except requests.Timeout as e:
            raise e

        coins_api_data = json.loads(response.content)"""

        coin_api_data = {'Bitcoin': {'eur': 95798.672, 'eur_market_cap': 1902933519720.6375, 'eur_24h_vol': 27492284005.581615, 'eur_24h_change': -0.030753219567922603}, 'Ethereum': {'eur': 2246.73, 'eur_market_cap': 271181748079.74295, 'eur_24h_vol': 11938328512.163212, 'eur_24h_change': -0.48479313103736404}, 'Tether': {'eur': 0.88, 'eur_market_cap': 134339110293.52779, 'eur_24h_vol': 44621288114.83347, 'eur_24h_change': -0.09100916684215263}, 'XRP': {'eur': 2.067, 'eur_market_cap': 121270656490.34639, 'eur_24h_vol': 1575569287.9324672, 'eur_24h_change': -0.42993475550965704}, 'BNB': {'eur': 593.152, 'eur_market_cap': 86531971689.52979, 'eur_24h_vol': 682430260.8701018, 'eur_24h_change': 0.8341650595658325}, 'Solana': {'eur': 154.903, 'eur_market_cap': 80567193231.94759, 'eur_24h_vol': 3828514317.679587, 'eur_24h_change': -2.7311551718872087}, 'USDC': {'eur': 0.879, 'eur_market_cap': 54286066984.31954, 'eur_24h_vol': 6656110126.452632, 'eur_24h_change': -0.10474936198268207}, 'Dogecoin': {'eur': 0.2, 'eur_market_cap': 29866498727.808483, 'eur_24h_vol': 1400823204.6250682, 'eur_24h_change': -2.9278318208948817}, 'Cardano': {'eur': 0.666, 'eur_market_cap': 24008881001.16213, 'eur_24h_vol': 665938675.1037793, 'eur_24h_change': -2.7095462422574923}, 'TRON': {'eur': 0.238, 'eur_market_cap': 22565583925.355022, 'eur_24h_vol': 596524011.9675951, 'eur_24h_change': 0.8608837882686703}, 'Lido Staked Ether': {'eur': 2244.873, 'eur_market_cap': 20196187391.92352, 'eur_24h_vol': 23448634.14992499, 'eur_24h_change': -0.3583299951810851}, 'Wrapped Bitcoin': {'eur': 95530.373, 'eur_market_cap': 12295870784.195463, 'eur_24h_vol': 224877755.90765813, 'eur_24h_change': -0.010454449368517424}, 'Sui': {'eur': 3.19, 'eur_market_cap': 10644852248.89445, 'eur_24h_vol': 922845327.9982433, 'eur_24h_change': -1.1252597562799604}, 'Hyperliquid': {'eur': 30.225, 'eur_market_cap': 10092515631.838161, 'eur_24h_vol': 298262731.39969575, 'eur_24h_change': -0.5115728620700346}, 'Wrapped stETH': {'eur': 2699.358, 'eur_market_cap': 9427832058.704563, 'eur_24h_vol': 17639005.937812123, 'eur_24h_change': -0.6469364077902491}}
        coin_insert_data = self._prepare_api_data(coin_api_data)

        return coin_insert_data

    def _prepare_coint_list_param(self, coins_list : str) -> str:
        coins_list_param = [self._process_spaces(coin) for coin in coins_list]  # process coinnames with spaces
        coins_list_param = "%2C".join(coins_list_param)  # build string param with commas

        return coins_list_param

    def _process_spaces(self, coin: str) -> str:
        """
        process a list of coin names in a the way coingecko processes a list of coins
        """
        if " " not in coin:
            return coin

        # coin name has spaces so interleave with space (%20)
        name_parts = coin.split(" ")
        coin_processed = "%20".join(name_parts)

        return coin_processed
    
    def _prepare_api_data(self, coin_api_data: dict[str, dict]) -> list[tuple]:
        """
        processes the api data into list of tuples that can be inserted into an sql source
        """
        # TODO probably wrap into dataclass with all data of a coin
        coins_list = list(coin_api_data.keys())
        
        coins_insert_data = []
        for name in coins_list:
            api_data = coin_api_data[name]
            coins_insert_data.append(
                (
                    name,
                    api_data["eur"],
                    api_data["eur_24h_change"],
                    api_data["eur_24h_vol"],
                    api_data["eur_market_cap"]
                )
            )

        return coins_insert_data
