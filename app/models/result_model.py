class Result:
    def __init__(self, position, driver, constructor, time, points):
        self.position = position
        self.driver = driver
        self.constructor = constructor
        self.time = time
        self.points = points

    def to_dict(self):
        return {
            "position": self.position,
            "driver": self.driver.to_dict(),
            "constructor": self.constructor.to_dict(),
            "time": self.time,
            "points": self.points,
        }

    def __repr__(self):
        return f'<Result {self.position}: {self.driver.name} ({self.points} points)>'
