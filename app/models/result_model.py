from app.models.driver_model import Driver
from app.models.constructor_model import Constructor

class Result:
    def __init__(self, position: int, driver: Driver, constructor: Constructor, time: str, points: float):
        self.position = position
        self.driver = driver
        self.constructor = constructor
        self.time = time
        self.points = points

    def to_dict(self) -> dict:
        return {
            "position": self.position,
            "driver": self.driver.to_dict(),
            "constructor": self.constructor.to_dict(),
            "time": self.time,
            "points": self.points
        }