class Result:
    def __init__(self, race_id: str, position: int, driver_id: str, constructor_id: str, time: str, points: float):
        self.race_id = race_id
        self.position = position
        self.driver_id = driver_id
        self.constructor_id = constructor_id
        self.time = time
        self.points = points

    def to_dict(self) -> dict:
        return {
            "race_id": self.race_id,
            "position": self.position,
            "driver": self.driver_id,
            "constructor": self.constructor_id,
            "time": self.time,
            "points": self.points
        }