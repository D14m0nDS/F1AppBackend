from app.models.result_model import Result
from typing import List

class Race:
    def __init__(
        self,
        race_id: int,
        season: int,
        round: int,
        name: str,
        circuit_name: str,
        date: str,
        city: str,
        country: str,
        results: List[Result]
    ):
        self.id = race_id
        self.season = season
        self.round = round
        self.name = name
        self.circuit_name = circuit_name
        self.date = date
        self.city = city
        self.country = country
        self.results = results

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "season": self.season,
            "round": self.round,
            "name": self.name,
            "circuit_name": self.circuit_name,
            "date": self.date,
            "city": self.city,
            "country": self.country,
            "results": [result.to_dict() for result in self.results]
        }