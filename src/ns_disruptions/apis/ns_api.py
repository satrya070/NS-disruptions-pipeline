import json
import os

from dotenv import load_dotenv
from urllib import request

load_dotenv()


class nsAPI:
    def __init__(self):
        self.api_key = os.environ["NS_API_KEY"]
    
    def fetch_disruption_data(self) -> list[dict]:
        """
        fetches the disruptions data from the api and returns the raw data
        """
        url_params = "?isActive=true"  # must be set in url directly
        url = f"https://gateway.apiportal.ns.nl/disruptions/v3{url_params}"

        headers = {
            "Cache-control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        try:
            req = request.Request(url, headers=headers)
            response = request.urlopen(req)
            result = json.loads(response.read())
        except Exception as e:
            print("Data api extraction failed: ", e)
            raise e
        
        return result
