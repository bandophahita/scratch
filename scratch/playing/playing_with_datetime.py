#!/usr/bin/env python3

from datetime import time, timedelta, datetime, date
from zoneinfo import ZoneInfo


DEFAULT_TZ = ZoneInfo("US/Central")


print()


staffing_day_times = [
    (# 6 
        time(hour=22),
        time(hour=4),
    ),
    (# 6
        time(hour=4),
        time(hour=10),
    ),
    (# 6
        time(hour=10),
        time(hour=16),
    ),
    (# 6
        time(hour=16),
        time(hour=22),
    ),
]

ARBITRARY_DATE = date(1970, 1, 1)
NOW = datetime.now(tz=DEFAULT_TZ)

def convert_times_to_datetime(times: list[tuple[time, time]]) -> list[tuple[datetime, datetime]]:
    s1 = times[0][0]
    cs1 = datetime.combine(ARBITRARY_DATE, s1)
    time.replace()
    
    # for pairs in 
    
    return converted
