from datetime import timedelta, datetime

from scratch.autofill_timetracking.readabledelta import to_string, ABBREV, SHORT, NORMAL, HOURS


T1 = 60 * 60 * 1 # 3600
T2 = 60 * 60 * 2 # 7200
T3 = 60 * 60 * 3 # 10800
T4 = 60 * 60 * 4 # 14400
T5 = 60 * 60 * 5 # 18000
T6 = 60 * 60 * 6 # 21600
T7 = 60 * 60 * 7 # 25200
T8 = 60 * 60 * 8 # 28800
T9 = 60 * 60 * 9 # 32400
T10 = 60 * 60 * 10 # 36000
T11 = 60 * 60 * 11 # 39600


def checkit(
    paid_delta: timedelta,
    # scheduled_hours: timedelta,
    period_crossed: datetime,
    shift_start_in_local: datetime,
    shift_end_in_local: datetime,
):
    scheduled_hours = shift_end_in_local - shift_start_in_local
    
    if paid_delta < scheduled_hours:
        if scheduled_hours <= timedelta(hours=4):
            hours_before_period = min(period_crossed - shift_start_in_local, paid_delta)
            hours_after_period = paid_delta - hours_before_period
        else:
            time_before = period_crossed - shift_start_in_local
            time_after = shift_end_in_local - period_crossed
            remove_hours_before = time_before >= timedelta(hours=4)
            break_time = scheduled_hours - paid_delta

            if remove_hours_before:
                hours_before_period = max(timedelta(hours=0), time_before - break_time)
                hours_after_period = paid_delta - hours_before_period
            else:
                hours_after_period = max(timedelta(hours=0), time_after - break_time)
                hours_before_period = paid_delta - hours_after_period
        
        return hours_before_period, hours_after_period
    else:
        raise Exception("Unhandled")


paid1 = timedelta(hours=1)
paid2 = timedelta(hours=2)
paid3 = timedelta(hours=3)
paid4 = timedelta(hours=4)
paid5 = timedelta(hours=5)
paid6 = timedelta(hours=6)
paid7 = timedelta(hours=7)
paid8 = timedelta(hours=8)
paid9 = timedelta(hours=9)

cross = datetime(2024, 7, 10) # midnight
shift_start = datetime(2024, 7, 9, 19)
shift_end = datetime(2024, 7, 10, 5)

schedhrs = shift_end - shift_start
fmt = "%m/%d/%Y %H:%M"

cases = [
    (paid1, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid1, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid1, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid1, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid1, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid1, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid1, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid1, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid1, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),
    
    (paid2, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid2, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid2, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid2, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid2, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid2, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid2, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid2, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid2, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),
    
    (paid3, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid3, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid3, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid3, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid3, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid3, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid3, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid3, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid3, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid4, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid4, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid4, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid4, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid4, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid4, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid4, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid4, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid4, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid5, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid5, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid5, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid5, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid5, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid5, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid5, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid5, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid5, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid6, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid6, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid6, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid6, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid6, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid6, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid6, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid6, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid6, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid7, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid7, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid7, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid7, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid7, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid7, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid7, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid7, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid7, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid8, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid8, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid8, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid8, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid8, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid8, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid8, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid8, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid8, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),

    (paid9, cross, cross - timedelta(hours=1), cross + timedelta(hours=9)),
    (paid9, cross, cross - timedelta(hours=2), cross + timedelta(hours=8)),
    (paid9, cross, cross - timedelta(hours=3), cross + timedelta(hours=7)),
    (paid9, cross, cross - timedelta(hours=4), cross + timedelta(hours=6)),
    (paid9, cross, cross - timedelta(hours=5), cross + timedelta(hours=5)),
    (paid9, cross, cross - timedelta(hours=6), cross + timedelta(hours=4)),
    (paid9, cross, cross - timedelta(hours=7), cross + timedelta(hours=3)),
    (paid9, cross, cross - timedelta(hours=8), cross + timedelta(hours=2)),
    (paid9, cross, cross - timedelta(hours=9), cross + timedelta(hours=1)),
]
STYLE = SHORT

def docase(case: tuple[timedelta, datetime, datetime, datetime]):
    paid, cross, start, end = case
    before, after = checkit(*case)
    p = to_string(paid, short=STYLE, keys=[HOURS], showzero=True)
    c = cross.strftime(fmt)
    s = start.strftime(fmt)
    e = end.strftime(fmt)
    b = to_string(before, short=STYLE, keys=[HOURS], showzero=True)
    a = to_string(after, short=STYLE, keys=[HOURS], showzero=True)
    t = to_string(end - start, short=STYLE, keys=[HOURS], showzero=True)
    bd = to_string(cross - start, short=STYLE, keys=[HOURS], showzero=True)
    ad = to_string(end - cross, short=STYLE, keys=[HOURS], showzero=True)
    print(f"{p:<5} paid, {s} - {e} : {t}  {bd:<5} / {ad:<5}  ===>  {b:<5} / {a:<5}")


for case in cases:
    docase(case)


rt1 = checkit(paid4, cross, shift_start, shift_end)

print()
