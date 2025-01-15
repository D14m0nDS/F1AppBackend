from abc import ABC, abstractmethod

class RaceRepositoryInterface(ABC):
    @abstractmethod
    def find_by_year_and_round(self, year, round):
        pass

    def get_schedule(self):
        pass