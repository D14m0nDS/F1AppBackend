from abc import ABC, abstractmethod


class DriverRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, driver_id):
        pass

    @abstractmethod
    def get_all_drivers(self, season: int):
        pass

    @abstractmethod
    def get_driver_standings(self, season: int):
        pass

