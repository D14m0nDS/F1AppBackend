import pandas as pd
from fastf1 import get_event_schedule, get_event
from fastf1.ergast import Ergast
from datetime import datetime

from app.models.race_model import Race
from app.models.result_model import Result
from app.repositories.race_repository import RaceRepositoryInterface

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_season_and_round(self, season, round):

        event = get_event(season, round)

        session = event.get_session("R")
        session.load()

        session_results = session.results
        race = Race(
            race_id=event['OfficialEventName'],
            season=season,
            round=round,
            name=event['EventName'],
            circuit_name=self.__find_circuit_by_location(season, event['Location']),
            date=event['EventDate'],
            city=event['Location'],
            country=event['Country'],
            results=[]
            )
        for _, result in session_results.iterrows():
            race.results.append(Result(
                race_id=event['OfficialEventName'],
                driver_id=result['DriverId'],
                driver_name=result['FullName'],
                constructor_id=result['TeamId'],
                constructor_name=result['TeamName'],
                position=float(result['Position']),
                points=float(result['Points']),
                time=str(result['Time']) if not pd.isna(result['Time']) else None,
                status=result['Status']
            ))

        return race.to_dict()

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