class Driver:

    def __init__(self, driver_id: str, name: str, age: int, number: int, constructor_id: str, points: float, results: list):
        self.id = driver_id
        self.name = name
        self.age = age
        self.number = number
        self.constructor_id = constructor_id
        self.points = points
        self.results = results

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "number": self.number,
            "constructor": self.constructor_id,
            "points": self.points,
            "results": [result.to_dict() for result in self.results]
        }