from fastf1 import get_event_schedule
from fastf1.ergast import Ergast
from datetime import datetime

from app.models.race_model import Race
from app.repositories.race_repository import RaceRepositoryInterface
import pandas as pd

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_season_and_round(self, season, round):
        race = self.ergast.get_race_results(season=season, round=round)
        print(race)
        return race

    def __find_circuit_by_location(self, season, location):

        schedule = self.ergast.get_race_schedule(season=season-1, result_type="pandas")

        if schedule is not None and not schedule.empty:

            matching_race = schedule[schedule['locality'] == location]

            if not matching_race.empty:
                circuit_name = matching_race.iloc[0]['circuitName']
                return circuit_name

        return "Circuit name not found"

    def __serialize_schedule(self, schedule, season):
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        new_schedule = list()
        for _, row in schedule.iterrows():
            print(row)
            new_schedule.append(Race(
                race_id=row['OfficialEventName'],
                season=season,
                round=row['RoundNumber'],
                date=row['EventDate'],
                country=row['Country'],
                city=row['Location'],
                circuit_name=self.__find_circuit_by_location(season, row['Location']),
                name=row['EventName'],
                results=[]
            ).to_dict())

        return new_schedule

    def get_schedule(self):
        current_year = datetime.now().year
        schedule = get_event_schedule(year=current_year)
        new_schedule = self.__serialize_schedule(schedule=schedule, season=current_year)
        return new_schedule