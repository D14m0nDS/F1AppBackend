from fastf1.ergast import Ergast

from app.repositories.driver_repository import DriverRepositoryInterface


class DriverRepositoryImpl(DriverRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, driver_id):
        pass

    def get_all_drivers(self):
        pass

    def get_driver_standings(self):
        pass