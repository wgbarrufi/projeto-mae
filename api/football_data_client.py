import os
import requests

from dotenv import load_dotenv

load_dotenv()


class FootballDataClient:

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):

        self.api_key = os.getenv(
            "FOOTBALL_DATA_API_KEY"
        )

    @property
    def headers(self):

        return {
            "X-Auth-Token": self.api_key
        }

    def listar_partidas(self, competicao: str):

        url = f"{self.BASE_URL}/competitions/{competicao}/matches"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()