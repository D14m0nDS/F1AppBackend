class Result:
    def __init__(
            self,
            race_id: str,
            position: float,
            driver_id: str,
            driver_name: str,
            constructor_id: str,
            constructor_name: str,
            time: str,
            points: float,
            status: str,
    ):
        self.race_id = race_id
        self.position = position
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.constructor_id = constructor_id
        self.constructor_name = constructor_name
        self.time = time
        self.points = points
        self.status = status

    def to_dict(self) -> dict:
        return {
            "race_id": self.race_id,
            "position": self.position,
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "constructor_id": self.constructor_id,
            "constructor_name": self.constructor_name,
            "time": self.time,
            "points": self.points,
            "status": self.status
        }