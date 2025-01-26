class DriverInfo:

    def __init__(self, driver_id: str, name: str, age: int, number: int, nationality: str, constructor_id: str, constructor_name: str, headshot_url: str):
        self.id = driver_id
        self.name = name
        self.age = age
        self.number = number
        self.nationality = nationality
        self.constructor_id = constructor_id
        self.constructor_name = constructor_name
        self.headshot_url = headshot_url

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "number": self.number,
            "nationality": self.nationality,
            "constructor": self.constructor_id,
            "constructor_name": self.constructor_name,
            "headshot_url": self.headshot_url
        }