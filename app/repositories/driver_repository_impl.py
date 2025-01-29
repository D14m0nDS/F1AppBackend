from datetime import datetime

import pandas as pd
from fastf1.ergast import Ergast

from app.models.driver_model import Driver
from app.models.driver_standings_model import DriverStandings
from app.repositories.driver_repository import DriverRepositoryInterface


class DriverRepositoryImpl(DriverRepositoryInterface):
    def __init__(self):
        self.ergast = Ergast()

    def find_by_id(self, driver_id: str) -> dict:
        try:
            current_year = 2024
            standings = self.ergast.get_driver_standings(season=current_year)

            df = standings.content[0]

            driver_data = df[df['driverId'] == driver_id]
            if driver_data.empty:
                return {"error": f"Driver {driver_id} not found in current season standings"}

            driver_info = driver_data.iloc[0]

            date_of_birth = driver_info['dateOfBirth']

            today = datetime.today()
            driver_age = today.year - date_of_birth.year - (
                        (today.month, today.day) < (date_of_birth.month, date_of_birth.day))

            headshot_url = self.build_f1_headshot_url(driver_info['givenName'], driver_info['familyName'])
            return Driver(
                driver_id=driver_info['driverId'],
                name=f"{driver_info['givenName']} {driver_info['familyName']}",
                constructor_id=driver_info['constructorIds'][0],
                constructor_name=driver_info['constructorNames'][0],
                number=int(driver_info['driverNumber']),
                age=driver_age,
                nationality=driver_info['driverNationality'],
                headshot_url=headshot_url,
                points = 0,
                results = []
            ).to_dict()



        except Exception as e:
            print(f"Error fetching driver data: {str(e)}")
            return {"error": f"Could not retrieve driver data: {str(e)}"}

    @staticmethod
    def build_f1_headshot_url(first_name: str, last_name: str) -> str:

        code = (first_name[:3] + last_name[:3]).upper() + "01"

        file_name = code.lower()

        first_letter = first_name[:1].upper() if first_name else "X"

        code = f"{code}_{first_name}_{last_name}"

        url = (
            "https://www.formula1.com/content/dam/fom-website/drivers/"
            f"{first_letter}/{code}/{file_name}.png.transform/1col/image.png"
        )
        return url

    def get_all_drivers(self, season: int) -> list[dict]:
        try:
            result = self.ergast.get_driver_standings(season=season)

            df = result.content[0]
            if df.empty:
                return []

            all_drivers = []

            for _, row in df.iterrows():
                driver_id = row['driverId']

                first_name = row.get('givenName', 'Unknown')
                last_name = row.get('familyName', 'Unknown')
                full_name = f"{first_name} {last_name}"

                date_of_birth = row.get('dateOfBirth', None)
                if date_of_birth is None or pd.isna(date_of_birth):
                    driver_age = 0
                else:
                    today = datetime.today()
                    driver_age = today.year - date_of_birth.year - (
                            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
                    )

                headshot_url = self.build_f1_headshot_url(first_name, last_name)

                constructor_ids = row.get('constructorIds', [])
                constructor_id = constructor_ids[0] if constructor_ids else "unknown"

                driver_number = row.get('driverNumber')
                driver_number = int(driver_number) if driver_number and not pd.isna(driver_number) else 0

                nationality = row.get('driverNationality', 'Unknown')

                points = row.get('points', 0.0)

                driver_obj = Driver(
                    driver_id=driver_id,
                    name=full_name,
                    age=driver_age,
                    number=driver_number,
                    constructor_id=constructor_id,
                    points=points,
                    results=[],
                    headshot_url=headshot_url,
                    nationality=nationality,
                    constructor_name=row.get('constructorNames', ['Unknown'])[0]
                )

                all_drivers.append(driver_obj)

            return [driver.to_dict() for driver in all_drivers]

        except Exception as e:
            print(f"Error fetching all drivers for season={season}: {str(e)}")
            return []

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