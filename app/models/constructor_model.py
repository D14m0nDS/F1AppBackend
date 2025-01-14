
class Constructor:
    def __init__(self, constructor_id, name, drivers, points):
        self.id = constructor_id
        self.name = name
        self.drivers = [driver for driver in drivers]
        self.points = points

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "drivers": [driver.to_dict() for driver in self.drivers],
            "points": self.points
        }

    def __repr__(self):
        return f'<Constructor {self.name}>'
