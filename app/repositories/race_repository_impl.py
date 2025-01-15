from fastf1.ergast import Ergast

from app.repositories.race_repository import RaceRepositoryInterface

class RaceRepositoryImpl(RaceRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_year_and_round(self, year, round):
        pass

    def get_schedule(self):
        pass