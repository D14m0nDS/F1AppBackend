from abc import ABC, abstractmethod

class RaceRepositoryInterface(ABC):
    @abstractmethod
    def find_by_season_and_round(self, season, round):
        pass

    @abstractmethod
    def get_schedule(self):
        pass