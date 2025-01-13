class Driver:

    def __init__(self, id, name, age, number, constructor, points):
        self.id = id
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
        }
    def __repr__(self):
        return f'<Driver {self.name}>'
