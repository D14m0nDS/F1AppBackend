from abc import ABC, abstractmethod


class ConstructorRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, constructor_id):
        pass

    @abstractmethod
    def get_all_constructors(self, season: int):
        pass

    @abstractmethod
    def get_constructor_standings(self, season: int):
        pass

