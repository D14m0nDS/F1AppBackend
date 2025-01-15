class Race:

    def __init__(self, race_id, season, round, name, circuit_name, date, city, country, laps, distance, results):
        self.id = race_id
        self.season = season
        self.round = round
        self.name = name
        self.circuit_name = circuit_name
        self.date = date
        self.city = city
        self.country = country
        self.laps = laps
        self.distance = distance
        self.total_distance = laps * distance
        self.results = results

    def to_dict(self):
        return {
            "id": self.id,
            "season": self.season,
            "round": self.round,
            "name": self.name,
            "date": self.date,
            "circuit_name": self.circuit_name,
            "city": self.city,
            "country": self.country,
            "laps": self.laps,
            "distance": self.distance,
            "total_distance": self.total_distance,
            "results": [result.to_dict() for result in self.results]
        }
    def __repr__(self):
        return f'<Race {self.name} ({self.date})>'