import pandas as pd
from fastf1.ergast import Ergast

from app.models.constructor_model import Constructor
from app.models.constructor_standings_model import ConstructorStandings
from app.repositories.constructor_repository import ConstructorRepositoryInterface


class ConstructorRepositoryImpl(ConstructorRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, constructor_id: str) -> dict:
        try:
            current_year = 2024
            constructor_standings = self.ergast.get_constructor_standings(season=current_year)

            if not constructor_standings.content:
                return {"error": "No constructor standings available."}

            df = constructor_standings.content[0]
            if df.empty:
                return {"error": f"No constructor data for season={current_year}"}

            constructor_data = df[df['constructorId'] == constructor_id]
            if constructor_data.empty:
                return {"error": f"Constructor {constructor_id} not found in standings for {current_year}"}

            row = constructor_data.iloc[0]
            name = row.get('constructorName', 'Unknown')
            nationality = row.get('constructorNationality', 'Unknown')
            points = row.get('points', 0.0)

            driver_standings = self.ergast.get_driver_standings(season=current_year)
            if driver_standings.content and not driver_standings.content[0].empty:
                driver_df = driver_standings.content[0]

                drivers_data = driver_df[
                    driver_df['constructorIds'].apply(lambda cids: constructor_id in cids)
                ]
                driver_ids = drivers_data['driverId'].unique().tolist()
            else:
                driver_ids = []

            constructor_obj = Constructor(
                constructor_id=constructor_id,
                name=name,
                nationality=nationality,
                driver_ids=driver_ids,
                points=float(points)
            )
            return constructor_obj.to_dict()

        except Exception as e:
            return {"error": f"Failed to fetch constructor {constructor_id}: {str(e)}"}

    def get_all_constructors(self, season: int) -> list[dict]:
        try:
            result = self.ergast.get_constructor_standings(season=season)
            if not result.content:
                return []

            constructors_df = result.content[0]
            if constructors_df.empty:
                return []

            driver_result = self.ergast.get_driver_standings(season=season)
            driver_df = None
            if driver_result.content and not driver_result.content[0].empty:
                driver_df = driver_result.content[0]

            all_constructors = []

            for _, row in constructors_df.iterrows():
                constructor_id = row.get('constructorId', 'unknown')
                name = row.get('constructorName', 'Unknown')
                nationality = row.get('constructorNationality', 'Unknown')
                points = row.get('points', 0.0)

                if driver_df is not None:
                    drivers_data = driver_df[
                        driver_df['constructorIds'].apply(lambda cids: constructor_id in cids)
                    ]
                    driver_ids = drivers_data['driverId'].unique().tolist()
                else:
                    driver_ids = []

                constructor_obj = Constructor(
                    constructor_id=constructor_id,
                    name=name,
                    nationality=nationality,
                    driver_ids=driver_ids,
                    points=float(points)
                )
                all_constructors.append(constructor_obj)

            return [constructor.to_dict() for constructor in all_constructors]

        except Exception as e:
            print(f"Error fetching all constructors for season={season}: {str(e)}")
            return []

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