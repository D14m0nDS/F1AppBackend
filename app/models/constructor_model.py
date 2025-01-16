from typing import List
from app.models.driver_model import Driver

class Constructor:
    def __init__(self, constructor_id: int, name: str, drivers: List[Driver], points: float):
        self.id = constructor_id
        self.name = name
        self.drivers = drivers
        self.points = points

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "drivers": [driver.to_dict() for driver in self.drivers],
            "points": self.points
        }