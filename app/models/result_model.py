class Result:
    def __init__(self, position, driver_id, driver_name, constructor, time, points):
        self.position = position
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.constructor = constructor
        self.time = time
        self.points = points

    def to_dict(self):
        return {
            "position": self.position,
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "constructor": self.constructor,
            "time": self.time,
            "points": self.points,
        }

    def __repr__(self):
        return f'<Result {self.position}: {self.driver_name} ({self.points} points)>'
