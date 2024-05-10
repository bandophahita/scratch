from __future__ import annotations

import calendar
from datetime import datetime, time as tdtime, timedelta
from typing import TYPE_CHECKING

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from screenpy.actions import Eventually, Pause, See, SeeAllOf, Silently
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy.resolutions import IsNot
from screenpy_selenium import Target
from screenpy_selenium.actions import Chain, Click, Enter, SwitchTo, Wait
from screenpy_selenium.questions import Element, Text
from screenpy_selenium.resolutions import IsClickable, Visible

from .. import readabledelta as rdd
from ..by import By

if TYPE_CHECKING:
    from screenpy import Actor

DETAIL_SUMMARY_HEADER = Target("Details Summary Header").located(
    By.xpath(
        "//div[@data-testid='issue.views.issue-details.issue-layout.container-right']"
        "//summary[contains(string(), 'Details')]"
    )
)

CLOCKIFY_SUMMARY_HEADER = Target("Clockify Summary Header").located(
    By.xpath(
        "//div[@data-testid='issue.views.issue-details.issue-layout.container-right']"
        "//summary[contains(string(), 'Clockify')]"
    )
)


CLOCKIFY_START_STOP_BUTTON = Target.the("Clockify Start/Stop Button").located_by(
    By.xpath(
        '//*[@data-testid="issue.views.issue-base.context.ecosystem.connect.field"]'
        '[contains(string(), "Start / Stop")]'
    )
)

CLOCKIFY_MANUAL_BUTTON = Target.the("Clockify Manual Button").located_by(
    (By.ID, "switchManual")
)

CLOCKIFY_TIMESHEET_FRAME = Target.the("Clockify_timesheet_frame").located_by(
    By.xpath(
        "//iframe[contains(@id, "
        '"clockify-timesheets-time-tracking-reports__clk-stopwatch")]'
    )
)

TIME_INPUT_FIELD = Target.the("Time Input Field").located_by(By.id("time-input"))

DATE_PICKER = Target.the("Date Picker").located_by(By.id("datepicker"))

FROM_TIME_FIELD = Target.the("From Time Field").located_by(By.id("timeFromManual"))

TO_TIME_FIELD = Target.the("To Time Field").located_by(By.id("timeToManual"))

ADD_TIME_BUTTON = Target.the("Add Time Button").located_by(By.id("addButtonManual"))

PROJECT_DROPDOWN = Target.the("Project Dropdown").located_by(
    By.id("select2-projectSelectManual-container")
)

PROJECT_DROPDOWN_SEARCH_FIELD = Target.the("Project Dropdown Search Rield").located_by(
    By.xpath('//input[@aria-controls="select2-projectSelectManual-results"]')
)

MESSAGE_MANUAL = Target.the("Message Manual").located_by(By.id("messageManual"))

# datepicker
MONTH_HEADER = Target.the("Month Header").located_by(
    By.xpath('//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-month"]')
)

YEAR_HEADER = Target.the("Year Header").located_by(
    By.xpath('//div[@id="ui-datepicker-div"]//span[@class="ui-datepicker-year"]')
)

PREV_MONTH = Target.the("Prev Month").located_by(By.xpath('//a[@title="Prev"]'))

NEXT_MONTH = Target.the("Next Month").located_by(By.xpath('//a[@title="Next"]'))


MONTH_MAP = {month: index for index, month in enumerate(calendar.month_name) if month}


class GetToJiraClockify(Performable):
    @beat("{} tries to GetToJiraClockify")
    def perform_as(self, actor: Actor):
        actor.will(Eventually(Silently(Click(DETAIL_SUMMARY_HEADER))))
        actor.will(Click(CLOCKIFY_SUMMARY_HEADER))
        actor.will(Silently(Wait.for_(CLOCKIFY_TIMESHEET_FRAME).to_appear()))
        actor.will(Silently(SwitchTo.the(CLOCKIFY_TIMESHEET_FRAME)))
        actor.will(Eventually(Silently(Click(CLOCKIFY_MANUAL_BUTTON))))
        actor.should(
            Silently(
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
        )


class LogTime(Performable):
    @beat("{} tries to LogTime {info_to_log}")
    def perform_as(self, actor: Actor):
        actor.will(ChooseDateFromPicker(self.date))
        hours_value = self._convert_timedelta(self.delta)

        actor.will(
            Chain(
                Click(FROM_TIME_FIELD),
                Enter(self.starttime.strftime("%H%M")).into_the(FROM_TIME_FIELD),
            )
        )
        actor.will(
            Chain(
                Click(TIME_INPUT_FIELD),
                Enter(hours_value).into_the(TIME_INPUT_FIELD),
            )
        )
        actor.will(
            Click(PROJECT_DROPDOWN),
            Eventually(Click(self.project_option)),
        )
        actor.will(Eventually(Click(ADD_TIME_BUTTON)))
        actor.will(Silently(Wait.for_(MESSAGE_MANUAL).to_be_clickable()))

    @property
    def info_to_log(self) -> str:
        hrs, mins, secs = LogTime.__convert_timedelta(self.delta)
        return f'{self.date.strftime("%m/%d/%Y")} {hrs:02}:{mins:02}:{secs:02}'

    @staticmethod
    def __convert_timedelta(td: timedelta) -> tuple[int, int, int]:
        """clockify needs the format to be HHMMSS"""
        data = rdd.split_timedelta_units(
            td, keys=[rdd.HOURS, rdd.MINUTES, rdd.SECONDS]
        )
        hrs = data[rdd.HOURS]
        if hrs > 24:
            raise ValueError("We should not be adding more than 24 hours")
        mins = data[rdd.MINUTES]
        secs = data[rdd.SECONDS]
        return hrs, mins, secs

    @staticmethod
    def _convert_timedelta(td: timedelta) -> str:
        hrs, mins, secs = LogTime.__convert_timedelta(td)
        return f"{hrs:02}{mins:02}{secs:02}"

    def __init__(
        self, date: datetime, delta: timedelta, starttime: tdtime, project: Target
    ):
        self.date = date
        self.delta = delta
        self.starttime = starttime
        self.project_option = project


class ChooseDateFromPicker(Performable):
    @beat("{} tries to ChooseDateFromPicker {dt_to_log}")
    def perform_as(self, actor: Actor):
        dt = self.dt

        actor.will(Silently(Eventually(Click(DATE_PICKER))))
        monthname = Silently(Text(MONTH_HEADER)).answered_by(actor)
        yeartext = Silently(Text(YEAR_HEADER)).answered_by(actor)
        dt_target_rounded = datetime(
            dt.year, dt.month, 1, dt.hour, dt.minute, dt.second
        )
        picker_dt = parse(f"{monthname} 1 {yeartext}")
        d = relativedelta(dt_target_rounded, picker_dt)
        month_offset = d.months + (12 * d.years)
        button = PREV_MONTH if month_offset < 0 else NEXT_MONTH
        clicks = abs(month_offset)

        for _cnt in range(clicks):
            actor.will(Silently(Eventually(Click(button))))
            actor.will(Silently(Pause(0.35).seconds_because("javascript updating")))

        monthname = Silently(Text(MONTH_HEADER)).answered_by(actor)
        if MONTH_MAP[monthname] != dt.month:
            raise Exception(
                f"logic error - should have gotten {dt.month}, "
                f"got {MONTH_MAP[monthname]} instead."
            )

        # @formatter:off
        # fmt: off
        DATE_BUTTON = Target.the(
            f"date {dt.day} button").located_by((
                By.XPATH,
                f'//td[@data-handler="selectDay"][string() = "{dt.day}"]'
                ))
        # fmt: on
        # @formatter:on

        actor.will(Silently(Eventually(Click(DATE_BUTTON))))
        actor.should(Silently(Eventually(See(Element(MONTH_HEADER), IsNot(Visible())))))

    @property
    def dt_to_log(self) -> str:
        return self.dt.strftime("%m/%d/%Y")

    def __init__(self, dt: datetime):
        self.dt = dt
