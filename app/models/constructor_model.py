from typing import List

class Constructor:
    def __init__(self, constructor_id: str, name: str, driver_ids: List[str], points: float):
        self.id = constructor_id
        self.name = name
        self.driver_ids = driver_ids
        self.points = points

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "drivers": [driver for driver in self.driver_ids],
            "points": self.points
        }