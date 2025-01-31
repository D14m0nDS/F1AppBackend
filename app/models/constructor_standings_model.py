class ConstructorStandings:
    def __init__(
            self,
            constructor_id: str,
            name: str,
            points: float,
            position: int,
            wins: int
    ):
        self.constructor_id = constructor_id
        self.name = name
        self.points = points
        self.position = position
        self.wins = wins

    def to_dict(self):
        return {
            "constructor_id": self.constructor_id,
            "name": self.name,
            "points": self.points,
            "position": self.position,
            "wins": self.wins
        }