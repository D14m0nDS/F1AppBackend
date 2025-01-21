import pandas as pd
from flask import jsonify

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from datetime import datetime
import fastf1
from fastf1 import get_event_schedule, get_session
from app.models.driver_model import Driver

fastf1.Cache.enable_cache('FastF1Cache')

def get_schedule():
    current_year = datetime.now().year
    schedule = get_event_schedule(year=current_year)

    # Convert schedule DataFrame to a list of dictionaries
    serialized_schedule = []
    for _, row in schedule.iterrows():
        event_dict = {
            "EventName": row['EventName'],  # Use column names as keys
            "EventDate": (
                row['EventDate'].isoformat()
                if pd.notna(row['EventDate'])
                else "Unknown"
            ),

        }
        serialized_schedule.append(event_dict)

    return jsonify(serialized_schedule)

# Test the function
print(get_schedule())