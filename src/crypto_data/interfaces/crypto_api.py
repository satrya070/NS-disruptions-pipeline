from abc import ABC, abstractmethod
#from typing import List, Dict


class CryptoAPI(ABC):
    @abstractmethod
    def fetch_coins_data(self, coins_list: list[str]) -> dict[str, dict]:
        pass

