import pandas as pd
from fastf1.ergast import Ergast

from app.models.constructor_standings_model import ConstructorStandings
from app.repositories.constructor_repository import ConstructorRepositoryInterface


class ConstructorRepositoryImpl(ConstructorRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, constructor_id):
        pass

    def get_all_constructors(self, season: int):
        pass

    def get_constructor_standings(self, season: int) -> list[dict]:
        try:

            result = self.ergast.get_constructor_standings(season=season)

            df = result.content[0]

            return [
                ConstructorStandings(
                    constructor_id=row['constructorId'],
                    name=row['constructorName'],
                    points=row['points'],
                    position=row['position'],
                    wins=row['wins']
                ).to_dict()
                for _, row in df.iterrows()
            ]

        except Exception as e:
            raise ValueError(f"Constructor standings error: {str(e)}")