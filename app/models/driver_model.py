class Driver:

    def __init__(self, driver_id, name, age, number, constructor, points):
        self.id = driver_id
        self.name = name
        self.age = age
        self.number = number
        self.constructor = constructor
        self.points = points

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "number": self.number,
            "constructor": self.constructor.to_dict(),
            "points": self.points
        }

    def __repr__(self):
        return f'<Driver {self.name}>'
