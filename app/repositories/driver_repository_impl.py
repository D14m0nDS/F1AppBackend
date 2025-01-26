from datetime import datetime

from fastf1.ergast import Ergast

from app.models.driver_info_model import DriverInfo
from app.models.driver_standings_model import DriverStandings
from app.repositories.driver_repository import DriverRepositoryInterface


class DriverRepositoryImpl(DriverRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, driver_id: str) -> dict:
        try:
            current_year = datetime.now().year
            standings = self.ergast.get_driver_standings(season=current_year-1)

            df = standings.content[0]

            driver_data = df[df['driverId'] == driver_id]
            if driver_data.empty:
                return {"error": f"Driver {driver_id} not found in current season standings"}

            driver_info = driver_data.iloc[0]

            date_of_birth = driver_info['dateOfBirth']

            today = datetime.today()
            driver_age = today.year - date_of_birth.year - (
                        (today.month, today.day) < (date_of_birth.month, date_of_birth.day))

            return DriverInfo(
                driver_id=driver_info['driverId'],
                name=f"{driver_info['givenName']} {driver_info['familyName']}",
                constructor_id=driver_info['constructorIds'][0],
                constructor_name=driver_info['constructorNames'][0],
                number=int(driver_info['driverNumber']),
                age=driver_age,
                nationality=driver_info['driverNationality'],
                headshot_url=""
            ).to_dict()



        except Exception as e:
            print(f"Error fetching driver data: {str(e)}")
            return {"error": f"Could not retrieve driver data: {str(e)}"}

    def get_all_drivers(self, season: int):
        pass

    def get_driver_standings(self, season: int) -> list[dict]:
        try:
            result = self.ergast.get_driver_standings(season=season)
            df = result.content[0]

            return [
                DriverStandings(
                    driver_id=row['driverId'],
                    name=f"{row['givenName']} {row['familyName']}",
                    constructor_id=row['constructorIds'][0],
                    constructor_name=row['constructorNames'][0],
                    points=row['points'],
                    position=row['position'],
                    wins=row['wins'],
                    driver_number=row['driverNumber']
                ).to_dict()
                for _, row in df.iterrows()
            ]

        except Exception as e:
            raise ValueError(f"Driver standings error: {str(e)}")