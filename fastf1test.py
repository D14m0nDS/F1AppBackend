import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from datetime import datetime
import fastf1
from fastf1 import get_event_schedule, get_session
from app.models.driver_model import Driver

fastf1.Cache.enable_cache('FastF1Cache')

def get_driver_standings() -> list:
    current_year = datetime.now().year
    schedule = get_event_schedule(current_year-2)

    # Debugging: print the first few rows of the schedule to verify structure
    print(schedule.head())

    if schedule.empty:
        raise ValueError("No races found in the current season.")

    # Ensure required columns are present
    if 'RoundNumber' not in schedule.columns:
        raise KeyError("The schedule is missing the 'RoundNumber' column.")

    # Access the last race of the season
    final_race = schedule.iloc[-1]  # Last race row
    season = final_race.get('Season', current_year)  # Use Season or default to current year
    round_number = final_race['RoundNumber']  # Round number of the last race

    # Get session data for the last race
    session = get_session(season, round_number, 'R')
    session.load()

    drivers = []
    for entry in session.results.iterrows():
        result = entry[1]

        driver = Driver(
            driver_id=result['Driver']['code'],  # Unique three-letter code
            name=f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
            age=None,  # Age calculation can be added if DOB is available
            number=result['Driver']['permanentNumber'],
            constructor_id=result['Constructor']['constructorId'],
            points=result['points'],
            results=[]  # Populate if you need detailed race results
        )
        drivers.append(driver.to_dict())

    return drivers


# Test the function
print(get_driver_standings())