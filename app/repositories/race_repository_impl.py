import pandas as pd
from fastf1.ergast import Ergast

from app.models.race_model import Race
from app.models.result_model import Result
from app.repositories.race_repository import RaceRepositoryInterface

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_season_and_round(self, season, round):

        results_response = self.ergast.get_race_results(season=season, round=round)

        race_info_response = self.ergast.get_race_schedule(season=season, round=round)

        schedule_first_row = race_info_response.iloc[0]

        results_df = results_response.content[0]
        if results_df.empty:
            return {
                "error": f"Results DataFrame is empty for season={season}, round={round}"
            }

        race_id = schedule_first_row.get('raceId') or f"{season}-{round}"
        race_name = schedule_first_row.get('raceName', 'Unknown')
        date = schedule_first_row.get('raceDate', 'Unknown')  # e.g. 'raceDate' or 'date'
        city = schedule_first_row.get('locality', 'Unknown')  # or 'location'
        country = schedule_first_row.get('country', 'Unknown')

        circuit_name = schedule_first_row.get('circuitName', 'Unknown')


        race = Race(
            race_id=str(race_id),
            season=season,
            round=round,
            name=race_name,
            circuit_name=circuit_name,
            date=str(date),
            city=city,
            country=country,
            results=[]
        )

        for _, row in results_df.iterrows():
            driver_id = row.get('driverId', 'unknown')
            driver_name = row.get('givenName') + ' ' + row.get('familyName')
            constructor_id = row.get('constructorId', 'unknown')
            constructor_name = row.get('constructorName', 'Unknown')

            position_raw = row.get('position', None)
            points_raw = row.get('points', 0)

            finish_time = row.get('totalRaceTime', None)
            if pd.isna(finish_time):
                finish_time = None

            status = row.get('status', 'Unknown')

            result_obj = Result(
                race_id=str(race_id),
                driver_id=driver_id,
                driver_name=driver_name,
                constructor_id=constructor_id,
                constructor_name=constructor_name,
                position=float(position_raw) if position_raw else None,
                points=float(points_raw),
                time=str(finish_time) if finish_time else None,
                status=status
            )
            race.results.append(result_obj)

        return race.to_dict()

    def __find_circuit_by_location(self, season, location):
        schedule_response = self.ergast.get_race_schedule(season=season)
        if not schedule_response.is_success or not schedule_response.content:
            return "Circuit name not found"

        schedule_df = schedule_response.content[0]  # or combine them if multiple
        if schedule_df.empty:
            return "Circuit name not found"

        matching_race = schedule_df[schedule_df['locality'] == location]
        if not matching_race.empty:
            return matching_race.iloc[0].get('circuitName', 'Unknown')

        return "Circuit name not found"

    def get_schedule(self):
        season = 2024

        schedule = self.ergast.get_race_schedule(season=season)



        new_schedule = []

        for _, row in schedule.iterrows():
            race_id = row.get('raceId') or f"{season}-{row.get('round')}"
            race_name = row.get('raceName', 'Unknown')
            round_number = row.get('round', 0)
            date = row.get('raceDate', 'N/A')
            city = row.get('locality', 'Unknown')
            country = row.get('country', 'Unknown')
            circuit_name = row.get('circuitName', 'Unknown')

            race_obj = Race(
                race_id=str(race_id),
                season=season,
                round=int(round_number),
                name=race_name,
                circuit_name=circuit_name,
                date=str(date),
                city=city,
                country=country,
                results=[]
            )
            new_schedule.append(race_obj.to_dict())

        return {
            "Schedule": {
                "season": season,
                "races": new_schedule
            }
        }
