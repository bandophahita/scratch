# noqa: E501
"""
Original inspiration from
https://github.com/wimglenn/readabledelta/blob/master/readabledelta.py
Converted to 3x python
"""
from __future__ import annotations

import warnings
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, TypeVar

from dateutil.relativedelta import relativedelta

if TYPE_CHECKING:
    from collections.abc import Sequence

NORMAL = 0
SHORT = 1
ABBREV = 2

YEARS = "years"
MONTHS = "months"
WEEKS = "weeks"
DAYS = "days"
HOURS = "hours"
MINUTES = "minutes"
SECONDS = "seconds"
MILLISECONDS = "milliseconds"
MICROSECONDS = "microseconds"


TIME_UNITS: dict[str, dict[str, str]] = {
    MICROSECONDS: {
        "plural": "microseconds",
        "singular": "microsecond",
        "abbrev": "µs",
        "short": "µsecs",
    },
    MILLISECONDS: {
        "plural": "milliseconds",
        "singular": "millisecond",
        "abbrev": "ms",
        "short": "msecs",
    },
    SECONDS: {
        "plural": "seconds",
        "singular": "second",
        "abbrev": "s",
        "short": "secs",
    },
    MINUTES: {
        "plural": "minutes",
        "singular": "minute",
        "abbrev": "m",
        "short": "mins",
    },
    HOURS: {"plural": "hours", "singular": "hour", "abbrev": "h", "short": "hrs"},
    DAYS: {"plural": "days", "singular": "day", "abbrev": "D", "short": "days"},
    WEEKS: {"plural": "weeks", "singular": "week", "abbrev": "W", "short": "wks"},
    MONTHS: {"plural": "months", "singular": "month", "abbrev": "M", "short": "mnths"},
    YEARS: {"plural": "years", "singular": "year", "abbrev": "Y", "short": "yrs"},
}

__version__ = "0.2.0"
TIMEDELTA_ALLOWED_UNITS = (
    YEARS,
    WEEKS,
    DAYS,
    HOURS,
    MINUTES,
    SECONDS,
    MILLISECONDS,
    MICROSECONDS,
)
# months are included here because relativedelta knows how to handle it.
RELATIVEDELTA_ALLOWED_UNITS = (
    YEARS,
    MONTHS,
    WEEKS,
    DAYS,
    HOURS,
    MINUTES,
    SECONDS,
    MICROSECONDS,
)


class ReadableDelta(timedelta):
    """
    Human readable version of timedelta
    """

    def __new__(cls: type[T], *args, **kwargs) -> T:
        years = kwargs.pop(YEARS, 0)
        if DAYS in kwargs:
            kwargs[DAYS] += 365 * years
        elif years:
            arg0 = args[0] if args else 0
            args = (365 * years + arg0,) + args[1:]
        # noinspection PyArgumentList
        self = timedelta.__new__(cls, *args, **kwargs)
        return self

    @classmethod
    def from_timedelta(cls: type[T], dt: timedelta) -> T:
        return cls(days=dt.days, seconds=dt.seconds, microseconds=dt.microseconds)

    def __unicode__(self):
        return to_string(self)

    __str__ = __unicode__


T = TypeVar("T", bound=ReadableDelta)


################################################################################
def normalize_timedelta_units(
    delta: timedelta, units: Sequence[str] | None = None
) -> dict[str, int]:
    """
    :param units: array of time magnitudes to be used for output
    """
    if units is None:
        units = TIMEDELTA_ALLOWED_UNITS

    delta = abs(delta)

    # timedeltas are normalised to just days, seconds, microseconds in cpython
    data = {}
    days = delta.days
    seconds = delta.seconds
    microseconds = delta.microseconds

    if YEARS in units:
        data[YEARS], days = divmod(days, 365)
    else:
        data[YEARS] = 0

    if WEEKS in units:
        data[WEEKS], days = divmod(days, 7)
    else:
        data[WEEKS] = 0

    if DAYS in units:
        data[DAYS] = days
    else:
        data[DAYS] = 0
        seconds += days * 86400  # 24 * 60 * 60

    if HOURS in units:
        data[HOURS], seconds = divmod(seconds, 60 * 60)
    else:
        data[HOURS] = 0

    if MINUTES in units:
        data[MINUTES], seconds = divmod(seconds, 60)
    else:
        data[MINUTES] = 0

    if SECONDS in units:
        data[SECONDS] = seconds
    else:
        data[SECONDS] = 0
        microseconds += seconds * 1000000  # 1000 * 1000

    if MILLISECONDS in units:
        data[MILLISECONDS], microseconds = divmod(microseconds, 1000)
    else:
        data[MILLISECONDS] = 0

    if MICROSECONDS in units:
        data[MICROSECONDS] = microseconds
    else:
        data[MICROSECONDS] = 0

    return data


################################################################################
def normalize_relativedelta_units(
    delta: relativedelta, units: Sequence[str] | None = None
):
    """
    :param units: array of time magnitudes to be used for output
    """
    if units is None:
        units = RELATIVEDELTA_ALLOWED_UNITS
    else:
        assert set(units).issubset(
            RELATIVEDELTA_ALLOWED_UNITS
        ), f"units can only be {RELATIVEDELTA_ALLOWED_UNITS}"

    delta = abs(delta)

    # timedeltas are normalised to just days, seconds, microseconds in cpython
    data = {}
    years = delta.years
    months = delta.months
    # weeks = delta.weeks
    days = delta.days
    hours = delta.hours
    minutes = delta.minutes
    seconds = delta.seconds
    microseconds = delta.microseconds

    # years are relative due to leapyear.... so unless they are in the delta..
    # we won't calculate them
    if YEARS in units:
        data[YEARS] = years
    else:
        data[YEARS] = 0
        months += years * 12

    # it's impossible to filter out months because there is no way to
    # convert them to smaller units without the relative dates.
    if MONTHS not in units and months:
        warnings.warn(
            "Cannot reduce months down to smaller units", Warning, stacklevel=1
        )
        # raise ValueError("Cannot reduce months down to smaller units")
    data[MONTHS] = months

    if WEEKS in units:
        data[WEEKS], days = divmod(days, 7)
    else:
        data[WEEKS] = 0

    if DAYS in units:
        data[DAYS] = days
    else:
        data[DAYS] = 0
        hours += days * 24

    if HOURS in units:
        data[HOURS] = hours
    else:
        data[HOURS] = 0
        minutes += hours * 60

    if MINUTES in units:
        data[MINUTES] = minutes
    else:
        data[MINUTES] = 0
        seconds += minutes * 60

    if SECONDS in units:
        data[SECONDS] = seconds
    else:
        data[SECONDS] = 0
        microseconds += seconds * 1000000  # 1000 * 1000

    if MICROSECONDS in units:
        data[MICROSECONDS] = microseconds
    else:
        data[MICROSECONDS] = 0

    return data


def is_negative_relativedelta(delta, dt=datetime(1970, 1, 1)):
    return (dt + delta) < (dt + relativedelta())


################################################################################
def to_string(
    delta: timedelta,
    style: int = NORMAL,
    include_sign: bool = True,
    units: Sequence[str] | None = None,
    showzero: bool = False,
) -> str:
    """
    Create Human readable timedelta string

    :param style: 1: uses short names, 2: uses abbreviation names
    :param include_sign: false will prevent sign from appearing
            allows you to create negative deltas but still have a human sentence like
            '2 hours ago' instead of '-2 hours ago'
    :param units: array of timeunits to be used for output
    :param showzero: prints out the values even if they are zero
    """
    negative = delta < timedelta(0)
    sign = "-" if include_sign and negative else ""
    delta = abs(delta)

    if units is None:
        units = TIMEDELTA_ALLOWED_UNITS
    else:
        assert set(units).issubset(
            TIMEDELTA_ALLOWED_UNITS
        ), f"keys can only be {TIMEDELTA_ALLOWED_UNITS}"

    data = normalize_timedelta_units(delta, units)

    output = []
    for k in units:
        val = data[k]
        if val == 0 and showzero is False:
            continue
        singular = val == 1
        tu = TIME_UNITS.get(k)

        if style == NORMAL:
            unit = tu.get("plural")
        elif style == SHORT:
            unit = tu.get("short")
        elif style == ABBREV:
            unit = tu.get("abbrev")
        else:
            raise ValueError(f"Invalid argument {style}")

        # make magnitude singular
        if style in [NORMAL, SHORT] and singular:
            unit = unit[:-1]

        output.append(f"{sign}{val} {unit}")
        # we only need to show the negative sign once.
        if val != 0:
            sign = ""

    if not output:
        result = str(delta)
    elif len(output) == 1:
        result = output[0]
    else:
        left, right = output[:-1], output[-1:]
        result = f"{', '.join(left)} and {right[0]}"

    return result


################################################################################
def extract_units(delta: timedelta, keys: Sequence[str] | None = None):
    """
    Given a timedelta, determine all the time magnitudes within said delta.
    """
    if keys is None:
        keys = TIMEDELTA_ALLOWED_UNITS
    data = normalize_timedelta_units(delta, keys)
    rkeys = []
    for key in keys:
        if data[key]:
            rkeys.append(key)
    return rkeys


################################################################################
def from_relativedelta(
    rdelta: relativedelta,
    style: int = NORMAL,
    include_sign: bool = True,
    units: Sequence[str] | None = None,
    showzero: bool = False,
) -> str:
    negative = is_negative_relativedelta(rdelta)
    sign = "-" if include_sign and negative else ""
    rdelta = abs(rdelta)

    if units is None:
        units = RELATIVEDELTA_ALLOWED_UNITS
    else:
        assert set(units).issubset(
            RELATIVEDELTA_ALLOWED_UNITS
        ), f"keys can only be {RELATIVEDELTA_ALLOWED_UNITS}"

    data = normalize_relativedelta_units(rdelta, units)

    output = []
    for k in units:
        val = data[k]
        if val == 0 and showzero is False:
            continue
        singular = val == 1
        tu = TIME_UNITS.get(k)

        if style == NORMAL:
            unit = tu.get("plural")
        elif style == SHORT:
            unit = tu.get("short")
        elif style == ABBREV:
            unit = tu.get("abbrev")
        else:
            raise ValueError(f"Invalid argument {style}")

        # make unit singular if needed
        if style in [NORMAL, SHORT] and singular:
            unit = unit[:-1]

        output.append(f"{sign}{val} {unit}")
        # we only need to show the negative sign once.
        if val != 0:
            sign = ""

    if not output:
        result = "now"
    elif len(output) == 1:
        result = output[0]
    else:
        left, right = output[:-1], output[-1:]
        result = f"{', '.join(left)} and {right[0]}"

    return result
