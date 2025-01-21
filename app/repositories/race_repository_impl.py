import fastf1
from fastf1 import get_event_schedule
from fastf1.ergast import Ergast
from datetime import datetime
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

        serialized_schedule = []
        for _, row in schedule.iterrows():
            event_dict = {
                "EventName": row['EventName'],
                "EventDate": (
                    row['EventDate'].isoformat() if pd.notna(row['EventDate']) else "Unknown"
                ),
                "Country": row['Country'],
                "Location": row['Location'],
                "CircuitName": self.__find_circuit_by_location(season, row['Location']),
                
            }
            serialized_schedule.append(event_dict)
        return serialized_schedule

    def get_schedule(self):
        current_year = datetime.now().year
        schedule = get_event_schedule(year=current_year)
        serialized_schedule = self.__serialize_schedule(schedule=schedule, season=current_year)
        return serialized_schedule