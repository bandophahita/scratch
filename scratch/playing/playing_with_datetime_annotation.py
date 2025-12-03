from datetime import datetime, timezone
from typing import Annotated, NewType
from zoneinfo import ZoneInfo

# Using NewType to distinguish aware datetimes
AwareDatetime = NewType("AwareDatetime", datetime)

def process_aware_time(dt: AwareDatetime):
    """Processes a timezone-aware datetime object."""
    print(f"Processing aware time: {dt}")

# Using Annotated for more specific timezone constraints (requires 'annotated-types' library for Timezone constraint)
# from annotated_types import Timezone
# SpecificLondonTime = Annotated[datetime, Timezone("Europe/London")]

# def process_london_time(dt: SpecificLondonTime):
#     print(f"Processing London time: {dt}")

if __name__ == "__main__":
    aware_dt = AwareDatetime(datetime.now(timezone.utc))
    not_aware_dt = datetime.now(timezone.utc)
    still_not_aware_dt = AwareDatetime(not_aware_dt)
    process_aware_time(aware_dt)
    
    # reveal_type(aware_dt)
    # Example of creating and using a timezone-aware datetime for annotation
    # london_dt = datetime.now(ZoneInfo("Europe/London"))
    # process_london_time(SpecificLondonTime(london_dt))