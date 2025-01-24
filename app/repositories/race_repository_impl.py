import pandas as pd
from fastf1 import get_event_schedule, get_event
from fastf1.ergast import Ergast
from datetime import datetime

from flask import session

from app.models.race_model import Race
from app.repositories.race_repository import RaceRepositoryInterface

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_season_and_round(self, season, round):

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)

        event = get_event(season, round)

        session = event.get_session("R")
        session.load()

        session_results = session.results


        print(session_results)
        return "Qj mi kura"

    def __find_circuit_by_location(self, season, location):

        schedule = self.ergast.get_race_schedule(season=season-1, result_type="pandas")

        if schedule is not None and not schedule.empty:

            matching_race = schedule[schedule['locality'] == location]

            if not matching_race.empty:
                circuit_name = matching_race.iloc[0]['circuitName']
                return circuit_name

        return "Circuit name not found"

    def __serialize_schedule(self, schedule, season):
        new_schedule = list()
        for _, row in schedule.iterrows():
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
        races = self.__serialize_schedule(schedule, season=current_year)
        return {
            "Schedule": {
                "season": current_year,
                "Races": races
            }
        }