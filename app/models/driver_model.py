from app.models.constructor_model import Constructor


class Driver:

    def __init__(self, driver_id: int, name: str, age: int, number: int, constructor: Constructor, points: float):
        self.id = driver_id
        self.name = name
        self.age = age
        self.number = number
        self.constructor = constructor
        self.points = points

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "number": self.number,
            "constructor": self.constructor.to_dict(),
            "points": self.points
        }