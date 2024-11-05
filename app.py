from flask import Flask
from flask_restful import Api, Resource

import fastf1

app = Flask(__name__)
api = Api(app)

drivers = {
    "Hamilton": {
        "team": "Mercedes",
        "wins": 100
    },
    "Verstappen": {
        "team": "Red Bull Racing",
        "wins": 50
    },
    "Norris": {
        "team": "McLaren",
        "wins": 10
    },
    "Ricciardo": {
        "team": "RB",
        "wins": 10
    },
    "Leclerc": {
        "team": "Ferrari",
        "wins": 25
    }
}

teams = {
    "Mercedes": {
        "team_principal": "Toto Wolff",
        "wins": 200
    },
    "Red Bull Racing": {
        "team_principal": "Christian Horner",
        "wins": 100
    },
    "McLaren": {
        "team_principal": "Zak Brown",
        "wins": 50
    },
    "Ferrari": {
        "team_principal": "Mattia Binotto",
        "wins": 150
    },
    "RB": {
        "team_principal": "Christian Horner",
        "wins": 100
    },
}


class Driver(Resource):
    def get(self, name):
        return {"driver": drivers[name]}



class Constructor(Resource):
    def get(self, name):
        return {"constructor": teams[name]}



class Standings(Resource):
    def get(self, type):
        return {"standings": ""}


api.add_resource(Driver, "/driver/<string:name>")
api.add_resource(Constructor, "/constructor/<string:name>")
api.add_resource(Standings, "/standings/<string:type>")

if __name__ == '__main__':
    app.run(debug=True)
