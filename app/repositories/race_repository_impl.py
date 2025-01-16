from fastf1.ergast import Ergast

from app.repositories.race_repository import RaceRepositoryInterface

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_season_and_round(self, season, round):
        race = self.ergast.get_race_results(season=season, round=round)
        print(race)
        return race

    def get_schedule(self):
        pass