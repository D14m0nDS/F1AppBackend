class DriverStandings:
    def __init__(self, driver_id, name, constructor_id, constructor_name, points, position, wins, driver_number):
        self.driver_id = driver_id
        self.name = name
        self.constructor_id = constructor_id
        self.constructor_name = constructor_name
        self.points = points
        self.position = position
        self.wins = wins
        self.driver_number = driver_number

    def to_dict(self):
        return {
            "driver_id": self.driver_id,
            "driver_name": self.name,
            "constructor_id": self.constructor_id,
            "constructor_name": self.constructor_name,
            "points": self.points,
            "position": self.position,
            "wins": self.wins,
            "driver_number": self.driver_number,
        }
