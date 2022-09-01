from __future__ import annotations

import calendar
from datetime import datetime
from datetime import time as tdtime
from datetime import timedelta
from typing import Union

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from pytz.tzinfo import BaseTzInfo, DstTzInfo, StaticTzInfo
from screenpy import Actor
from screenpy.actions import Eventually, Pause, See, SeeAllOf
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy.resolutions import IsNot
from screenpy_selenium import Target
from screenpy_selenium.actions import Chain, Click, Enter, SwitchTo
from screenpy_selenium.questions import Element, Text
from screenpy_selenium.resolutions import IsClickable, Visible
from selenium.webdriver.common.by import By

from autofill_timetracking import readabledelta as rdd


# @formatter:off
# fmt: off
class _UTCclass(BaseTzInfo):
    def localize(self, dt: datetime, is_dst: Union[bool, None] = ...) -> datetime: ...
    def normalize(self, dt: datetime) -> datetime: ...
    def tzname(self, dt: Union[datetime, None]) -> str: ...
    def utcoffset(self, dt: Union[datetime, None]) -> timedelta: ...
    def dst(self, dt: Union[datetime, None]) -> timedelta: ...


T_pytZone = Union[_UTCclass, StaticTzInfo, DstTzInfo]

CLOCKIFY_START_STOP_BUTTON = Target.the(
    f"clockify start stop button").located_by((
        By.XPATH,
        '//*[@data-testid="issue.views.issue-base.context.ecosystem.connect.field"][contains(string(), "Start / Stop")]'
        ))

CLOCKIFY_MANUAL_BUTTON = Target.the(
    f"clockify manual button").located_by((
        By.ID,
        'switchManual'
        ))

CLOCKIFY_TIMESHEET_FRAME = Target.the(
    f"clockify_timesheet_frame").located_by((
        By.XPATH,
        '//iframe[contains(@id, "clockify-timesheets-time-tracking-reports__clk-stopwatch")]'
        ))

TIME_INPUT_FIELD = Target.the(
    f"time input field").located_by((
        By.ID,
        'time-input'
        ))

DATE_PICKER = Target.the(
    f"date picker").located_by((
        By.ID,
        'datepicker'
        ))

FROM_TIME_FIELD = Target.the(
    f"from time field").located_by((
        By.ID,
        'timeFromManual'
        ))

TO_TIME_FIELD = Target.the(
    f"to time field").located_by((
        By.ID,
        'timeToManual'
        ))

ADD_TIME_BUTTON = Target.the(
    f"add time button").located_by((
        By.ID,
        'addButtonManual'
        ))

PROJECT_DROPDOWN = Target.the(
    f"project dropdown").located_by((
        By.ID,
        'select2-projectSelectManual-container'
        ))

PROJECT_DROPDOWN_SEARCH_FIELD = Target.the(
    f"project dropdown search field").located_by((
        By.XPATH,
        '//input[@aria-controls="select2-projectSelectManual-results"]'
        ))

NEXTGEN_PROJECT_OPTION = Target.the(
    f"nextgen project option").located_by((
        By.XPATH,
        '//*[@id="select2-projectSelectManual-results"]//li[string() = "A - NEXTGEN"]'
        ))

MESSAGE_MANUAL = Target.the(
    f"message manual").located_by((
        By.ID,
        'messageManual'
        ))

# datepicker
MONTH_HEADER = Target.the(
    f"month header").located_by((
        By.XPATH,
        '//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-month"]'
        ))

YEAR_HEADER = Target.the(
    f"year header").located_by((
        By.XPATH,
        '//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-year"]'
        ))

PREV_MONTH = Target.the(
    f"prev month").located_by((
        By.XPATH,
        '//a[@title="Prev"]'
        ))

NEXT_MONTH = Target.the(
    f"next month").located_by((
        By.XPATH,
        '//a[@title="Next"]'
        ))
# fmt: on
# @formatter:on

MONTH_MAP = {month: index for index, month in enumerate(calendar.month_name) if month}


class GetToJiraClockify(Performable):
    @beat("[TASK] {} attempts to GetToJiraClockify")
    def perform_as(self, actor: Actor):
        actor.attempts_to(Eventually(Click(CLOCKIFY_START_STOP_BUTTON)))
        actor.attempts_to(Eventually(SwitchTo.the(CLOCKIFY_TIMESHEET_FRAME)))
        actor.attempts_to(Eventually(Click(CLOCKIFY_MANUAL_BUTTON)))
        actor.should(
            Eventually(
                SeeAllOf(
                    (Element(TIME_INPUT_FIELD), IsClickable()),
                    (Element(DATE_PICKER), IsClickable()),
                    (Element(FROM_TIME_FIELD), IsClickable()),
                    (Element(TO_TIME_FIELD), IsClickable()),
                    (Element(ADD_TIME_BUTTON), IsClickable()),
                    (Element(PROJECT_DROPDOWN), IsClickable()),
                )
            )
        )
        return


class LogTimeInJiraClockify(Performable):
    @beat("[TASK] {} attempts to LogTimeInJiraClockify")
    def perform_as(self, actor: Actor):
        actor.attempts_to(ChooseDateFromPicker(self.date, self.tzone))
        hours_value = self._convert_timedelta(self.delta)

        actor.attempts_to(
            Chain(
                Click(FROM_TIME_FIELD),
                Enter(self.starttime.strftime("%H%M")).into_the(FROM_TIME_FIELD),
            )
        )
        actor.attempts_to(
            Chain(
                Click(TIME_INPUT_FIELD),
                Enter(hours_value).into_the(TIME_INPUT_FIELD),
            )
        )
        actor.attempts_to(
            Click(PROJECT_DROPDOWN),
            Eventually(Click(NEXTGEN_PROJECT_OPTION)),
        )
        actor.attempts_to(Eventually(Click(ADD_TIME_BUTTON)))
        actor.attempts_to(Eventually(See(Element(MESSAGE_MANUAL), IsClickable())))
        return

    @staticmethod
    def _convert_timedelta(td: timedelta) -> str:
        """clockify needs the format to be HHMMSS"""
        data = rdd.normalize_timedelta_units(
            td, units=[rdd.HOURS, rdd.MINUTES, rdd.SECONDS]
        )
        hrs = data[rdd.HOURS]
        if hrs > 24:
            raise ValueError("We should not be adding more than 24 hours")
        mins = data[rdd.MINUTES]
        secs = data[rdd.SECONDS]
        return f"{hrs:02}{mins:02}{secs:02}"

    def __init__(
        self, date: datetime, delta: timedelta, tzone: T_pytZone, starttime: tdtime
    ):
        self.date = date
        self.delta = delta
        # TODO: perhaps we can get the zone directly from the date object?
        self.tzone = tzone
        self.starttime = starttime


class ChooseDateFromPicker(Performable):
    @beat("[TASK] {} attempts to ChooseDateFromPicker")
    def perform_as(self, actor: Actor):
        dt = self.dt
        tzone = self.tzone

        actor.attempts_to(Eventually(Click(DATE_PICKER)))
        monthname = Text(MONTH_HEADER).answered_by(actor)
        yeartext = Text(YEAR_HEADER).answered_by(actor)
        dt_target_rounded = datetime(
            dt.year, dt.month, 1, dt.hour, dt.minute, dt.second, tzinfo=dt.tzinfo
        )
        picker_dt = tzone.localize(parse(f"{monthname} 1 {yeartext}"))

        d = relativedelta(dt_target_rounded.astimezone((tzone)), picker_dt)
        clicks = d.months + (12 * d.years)
        button = PREV_MONTH if clicks < 0 else NEXT_MONTH

        for cnt in range(abs(clicks)):
            actor.attempts_to(Eventually(Click(button)))
            actor.attempts_to(Pause(0.25).seconds_because(""))

        monthname = Text(MONTH_HEADER).answered_by(actor)
        if MONTH_MAP[monthname] != dt.month:
            raise Exception(
                f"logic error - should have gotten {dt.month}, got {MONTH_MAP[monthname]} instead."
            )

        # @formatter:off
        # fmt: off
        DATE_BUTTON = Target.the(
            f"date button").located_by((
                By.XPATH,
                f'//td[@data-handler="selectDay"][string() = "{dt.day}"]'
                ))
        # fmt: on
        # @formatter:on

        actor.attempts_to(Eventually(Click(DATE_BUTTON)))
        actor.should(Eventually(See(Element(MONTH_HEADER), IsNot(Visible()))))
        return

    def __init__(self, dt: datetime, tzone: T_pytZone):
        self.dt = dt
        # TODO: perhaps we can get the zone directly from the date object?
        self.tzone = tzone
