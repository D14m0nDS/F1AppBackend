from fastf1.ergast import Ergast

from app.repositories.constructor_repository import ConstructorRepositoryInterface


class ConstructorRepositoryImpl(ConstructorRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, constructor_id):
        pass

    def get_all_constructors(self):
        pass

    def get_constructor_standings(self):
        pass