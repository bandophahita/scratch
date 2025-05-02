from datetime import datetime, timedelta, timezone, UTC, tzinfo
from dateutil import tz
from functools import total_ordering
from zoneinfo import ZoneInfo

# NYC = tz.gettz('America/New_York')
# NYC = ZoneInfo('America/New_York')
CST2 = tz.gettz("US/Central")
CST = ZoneInfo("US/Central")

@total_ordering
class AbsoluteDateTime(datetime):
    """A version of datetime that uses only elapsed time semantics"""

    _utc_datetime_cache = None

    @property
    def _utc_datetime(self):
        if self._utc_datetime_cache is None:
            dt = datetime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
                tzinfo=self.tzinfo,
                fold=self.fold,
            )
            self._utc_datetime_cache = dt.astimezone(UTC)

        return self._utc_datetime_cache

    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self._utc_datetime, other)
        if self.tzinfo is not UTC:
            dt = dt.astimezone(self.tzinfo)

            # Required to support the case where tzinfo is None
            dt = dt.replace(tzinfo=self.tzinfo)
        return type(self).as_absolute_datetime(dt)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            # Use __add__ implementation if it's datetime and timedelta
            return self + (-1) * other
        else:
            return datetime.__sub__(self._utc_datetime, other.astimezone(UTC))

    def __eq__(self, other):
        return datetime.__eq__(self._utc_datetime, other.astimezone(UTC))

    def __lt__(self, other):
        return datetime.__lt__(self._utc_datetime, other.astimezone(UTC))

    @classmethod
    def as_absolute_datetime(cls, dt: datetime):
        """Construct an AbsoluteDatetime from any datetime subclass"""
        return cls(
            *dt.timetuple()[0:6],
            microsecond=dt.microsecond,
            tzinfo=dt.tzinfo,
            fold=dt.fold
        )


@total_ordering
class WallDateTime(datetime):
    """A version of datetime that uses only wall time semantics"""

    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self.replace(tzinfo=None), other)

        if self.tzinfo is not None:
            dt = dt.replace(tzinfo=self.tzinfo)

        return self.__class__.as_wall_datetime(dt)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            # Use __add__ implementation if it's datetime and timedelta
            return self + (-1) * other
        else:
            return datetime.__sub__(
                self.replace(tzinfo=None), other.replace(tzinfo=None)
            )

    def __eq__(self, other):
        return datetime.__eq__(
            self.replace(tzinfo=None), other.replace(tzinfo=None)
        )

    def __lt__(self, other):
        return datetime.__lt__(
            self.replace(tzinfo=None), other.replace(tzinfo=None)
        )

    @classmethod
    def as_wall_datetime(cls, dt: datetime):
        """Construct a WallDateTime from any datetime subclass"""
        return cls(
            *dt.timetuple()[0:6],
            microsecond=dt.microsecond,
            tzinfo=dt.tzinfo,
            fold=dt.fold
        )

################################################################################
def wall_add(dt, other):
    return dt + other

def wall_sub(dt, other):
    if isinstance(other, timedelta):
        return wall_add(dt, -1 * other)

    return dt.replace(tzinfo=None)- other.replace(tzinfo=None)


def absolute_add(dt, other):
    return (dt.astimezone(UTC) + other).astimezone(dt.tzinfo)

def absolute_sub(dt, other):
    if isinstance(other, timedelta):
        return absolute_add(dt, -1 * other)

    return (dt.astimezone(UTC) - other.astimezone(UTC))

def line():
    return "-"*80

################################################################################
dt1 = datetime(2024, 3, 9, 13, tzinfo=CST)  # day before DST transition
dt2 = dt1 + timedelta(days=1)
print(dt1)
print(wall_add(dt1, timedelta(days=1)))
print(absolute_add(dt1, timedelta(days=1)))

print(line())
dt3 = datetime(2018, 3, 10, 13, 30, tzinfo=CST)
dt4 = datetime(2018, 3, 11, 8, 30, tzinfo=CST)

print(wall_sub(dt4, dt3))
# 19:00:00
print(absolute_sub(dt4, dt3))
# 18:00:00

print(line())
dt5 = datetime(2024, 3, 9, 13, 30, tzinfo=CST)
dt6 = datetime(2024, 3, 10, 8, 30, tzinfo=CST)

print(wall_sub(dt6, dt5))
# 19:00:00
print(absolute_sub(dt6, dt5))
# 18:00:00

utc1 = ZoneInfo("UTC")
utc2 = UTC
print(line())


# dt_start = datetime(2025, 3, 9, 0, tzinfo=CST)  # midnight on the day DST occurs
# dt_end = datetime(2025, 3, 9, 3, tzinfo=CST)  # 3am after DST transition 

dt_start = AbsoluteDateTime(2025, 3, 9, 0, tzinfo=CST)
dt_end = AbsoluteDateTime(2025, 3, 9, 3, tzinfo=CST)

# dt_start = WallDateTime(2025, 3, 9, 0, tzinfo=CST)
# dt_end = WallDateTime(2025, 3, 9, 3, tzinfo=CST)

print(dt_end-dt_start)
print(wall_sub(dt_end, dt_start))
print(absolute_sub(dt_end, dt_start))




print(line())