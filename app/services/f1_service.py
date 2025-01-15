from datetime import datetime
from app.repositories.driver_repository import DriverRepositoryInterface as DriverRepository
from app.repositories.constructor_repository import ConstructorRepositoryInterface as ConstructorRepository
from app.repositories.race_repository import RaceRepositoryInterface as RaceRepository

class F1Service:
    def __init__(self, driver_repository: DriverRepository, constructor_repository: ConstructorRepository, race_repository: RaceRepository):
        self.driver_repository = driver_repository
        self.constructor_repository = constructor_repository
        self.race_repository = race_repository

    def get_driver_standings(self):
        driver_standings = self.driver_repository.get_driver_standings()
        return driver_standings

    def get_constructor_standings(self):
        constructor_standings = self.constructor_repository.get_constructor_standings()
        return constructor_standings

    def get_schedule(self):
        schedule = self.race_repository.get_schedule()
        return schedule

    def get_race(self, year, round):
        current_year = datetime.now().year
        if year < 1950 or year > current_year or round < 1 or round > 24:
            raise ValueError(f"Invalid year '{year}' or round '{round}'. Year must be between 1950 and {current_year}, and round must be between 1 and 24.")
        return self.race_repository.find_by_year_and_round(year, round)

    def get_driver(self, driver_id):
        return self.driver_repository.find_by_id(driver_id)

    def get_constructor(self, constructor_id):
        return self.constructor_repository.find_by_id(constructor_id)

    def get_all_drivers(self):
        return self.driver_repository.get_all_drivers()

    def get_all_constructors(self):
        return self.constructor_repository.get_all_constructors()