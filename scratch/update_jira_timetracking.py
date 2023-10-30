#!/usr/bin/env python3
"""
This script works on cloud based Jira projects which also utilize clockify.
This version currently assumes you login to Jira via google SSO.
Other methods could be added.

It is meant to fill in the remaining time of a given day for a single ticket.

Typical Usage:

    update_jira_timetracking.py 2022-09-09

First Time Usage Example:

    update_jira_timetracking.py 2022-09-09 -u USER -p PASS -U https://site.atlassian.net/browse/TICKET-1 -P MYPROJ -O f5e2cf77e89a178127ab17a5ac50370b -A a2db76a60306ba3e6e3029c28f0402b

Things you will need to run this script:
 - Your clockify API key
 - Your google user/pass and OTP secret.
    (the value that you QR code scan to add 2FA on your phone)

"""  # noqa: E501

from __future__ import annotations

import argparse
import calendar
from datetime import datetime, timedelta

import keyring
import pytz
from autofill_timetracking import readabledelta as rdd
from autofill_timetracking.ability import Authenticate, ManageBrowserLocalStorage
from autofill_timetracking.actions import (
    GetToJiraClockify,
    LoginToJiraViaJumpCloud,
    LoginToJiraViaGoogle,
    LogTimeInJiraClockify,
)
from autofill_timetracking.by import By
from autofill_timetracking.logger import create_logger, enable_logger
from clockify_api_client.client import ClockifyAPIClient  # type: ignore
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from screenpy import Actor, settings
from screenpy.narration.stdout_adapter import StdOutAdapter, StdOutManager
from screenpy.pacing import the_narrator
from screenpy_pyotp.abilities import AuthenticateWith2FA
from screenpy_selenium import Target
from screenpy_selenium.abilities import BrowseTheWeb
from setup_selenium import Browser, SetupSelenium, set_logger

# uncomment to use our own logger that handles file & line better
logger = create_logger("screenpy2")
the_narrator.adapters = [StdOutAdapter(StdOutManager(logger))]
set_logger(logger)
enable_logger(logger)


MONTH_MAP = {month: index for index, month in enumerate(calendar.month_name) if month}
FMT = "%Y-%m-%dT%H:%M:%SZ"
KEY = "autofill_script"
Namespace = argparse.Namespace
T_default = str | None


def setup_selenium():
    settings.TIMEOUT = 30
    browser = Browser.CHROME
    headless = False
    driver = SetupSelenium.create_driver(browser, headless)
    driver.set_window_size(1600, 1080)
    driver.set_window_position(0, 0)
    return driver


def get_hours_total_for_day(cclient: ClockifyAPIClient, dt: datetime) -> timedelta:
    """
    find out how many hours are currently logged for a given time period via clockify
    """
    params = {
        "start": dt.astimezone(pytz.UTC).strftime(FMT),
        "end": (dt + relativedelta(days=1)).astimezone(pytz.UTC).strftime(FMT),
    }
    user = cclient.users.get_current_user()
    workspaceid = user["defaultWorkspace"]
    userid = user["id"]
    time_entries: list[dict] = cclient.time_entries.get_time_entries(
        workspaceid, userid, params=params
    )

    def get_total_hours(time_entries: list[dict]) -> timedelta:
        total = timedelta()
        for time_entry in time_entries:
            times = time_entry["timeInterval"]
            start = parse(times["start"])
            end = parse(times["end"])
            total += end - start
        return total

    return get_total_hours(time_entries)


def convert_timedelta(td: timedelta) -> str:
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


################################################################################
def in_keychain(keyname: str | None) -> str:
    return f"{'in keychain' if keyname else 'NOT IN KEYCHAIN'}"


def set_keychain(
    args: Namespace,
    default: T_default,
    value: str,
    key: str,
    keyname: str | None = None,
):
    keyname = keyname or key
    if (default is None or default != value) and key in args:
        keyring.set_password(KEY, keyname, f"{value}")


def get_args_val(
    args: Namespace, default: T_default, key: str, keyname: str | None = None
) -> str:
    keyname = keyname or key
    if default is None and key not in args:
        raise ValueError(f"Could not find {KEY}:{keyname} in keychain")
    value = getattr(args, key) if key in args else default
    return value


def get_keychain_val(
    args: Namespace, default: T_default, key: str, keyname: str | None = None
) -> str:
    keyname = keyname or key
    value = get_args_val(args, default, key, keyname)
    set_keychain(args, default, value, key, keyname)
    return value


################################################################################
if __name__ == "__main__":
    desc = """Update Jira Clockify time tracking.
    This script will utilize the keychain to store and read critical values like api
    keys.
    It's possible for more than one user to run this script on the same machine.  Each
    user's values are stored seperately in the keychain.

    To update the project in keychain
    update_jira_timetracking.py -P PROJECT_NAME YYYY-MM-DD YYYY-MM-DD

    update password in keychain
    update_jira_timetracking.py -p password YYYY-MM-DD YYYY-MM-DD

    update api key in keychain
    update_jira_timetracking.py -A APIKEY YYYY-MM-DD YYYY-MM-DD


    When your gmail password changes, you'll need to update the password stored in the
    keychain.  Simply adding the parameter and the password to the commandline
    will do this

    """
    parser1 = argparse.ArgumentParser(add_help=False)

    keyname_user = "username"
    keyname_url = "url_ticket"
    keyname_timezone = "timezone"
    keyname_hours = "hours"
    keyname_daystart = "daystart"
    keyname_project = "project"

    USERNAME = "username"
    PASSWORD = "password"
    SETKEYS = "setkeys"
    TIMEZONE = "timezone"
    DAYSTART = "daystart"
    PROJECT = "project"
    API = "api"
    URL = "url"
    OTP = "otp"
    DATE = "date"
    HOURS = "hours"

    default_timezone = "US/Central"
    default_daystart = "08:00"
    default_hours = "8"
    default_user = keyring.get_password(KEY, keyname_user)
    default_url = keyring.get_password(KEY, keyname_url)
    default_project = keyring.get_password(KEY, keyname_project)

    parser1.add_argument(
        "-u",
        default=argparse.SUPPRESS,
        dest=USERNAME,
        metavar="USER",
        help=f"(default: {default_user})",
    )

    args1, unknown = parser1.parse_known_args()

    parser2 = argparse.ArgumentParser(
        description=desc,
        parents=[parser1],
        add_help=False,
    )

    username = get_args_val(args1, default_user, USERNAME, keyname_user)

    keyname_pass = username
    keyname_otp = f"otp_jc_{username}"
    # keyname_otp = f"otp_{username}"
    keyname_api = f"clockify_api_key_{username}"

    default_pass = keyring.get_password(KEY, keyname_pass)
    default_otp = keyring.get_password(KEY, keyname_otp)
    default_api = keyring.get_password(KEY, keyname_api)

    parser2.add_argument(
        dest=DATE,
        metavar="YYYY-MM-DD",
        nargs="*",
        help="(required) date in format YYYY-MM-DD. Two dates will produce a range.",
    )

    parser2.add_argument(
        "-p",
        default=argparse.SUPPRESS,
        dest=PASSWORD,
        metavar="PASS",
        help=f"(default: {in_keychain(default_pass)})",
    )

    parser2.add_argument(
        "-U",
        default=argparse.SUPPRESS,
        dest=URL,
        help=f"Url of jira ticket (default: {default_url})",
    )

    parser2.add_argument(
        "-P",
        default=argparse.SUPPRESS,
        dest=PROJECT,
        help=f"Project name (default: {default_project})",
    )

    parser2.add_argument(
        "--otp",
        default=argparse.SUPPRESS,
        dest=OTP,
        help=f"one time password secret (default: {in_keychain(default_otp)})",
    )

    parser2.add_argument(
        "-A",
        default=argparse.SUPPRESS,
        dest=API,
        metavar="API_KEY",
        help=f"clockify api key (default: {in_keychain(default_api)})",
    )

    parser2.add_argument(
        "-S",
        default=default_daystart,
        dest=DAYSTART,
        metavar="HH:MM",
        help=f"Start of the workday. (default: {default_daystart})",
    )

    parser2.add_argument(
        "-H",
        default=default_hours,
        dest=HOURS,
        help=f"(default: {default_hours})",
    )

    parser2.add_argument(
        "-Z",
        default=default_timezone,
        dest=TIMEZONE,
        help=f"(default: {default_timezone})",
    )

    parser2.add_argument(
        "-h",
        "--help",
        action="help",
        help="show this help message and exit",
    )

    args = parser2.parse_args()

    ################################################################################
    set_keychain(args, default_user, username, USERNAME, keyname_user)

    password = get_keychain_val(args, default_pass, PASSWORD, keyname_pass)
    url = get_keychain_val(args, default_url, URL, keyname_url)
    otp = get_keychain_val(args, default_otp, OTP, keyname_otp)
    api = get_keychain_val(args, default_api, API, keyname_api)
    project = get_keychain_val(args, default_project, PROJECT, keyname_project)

    timezone = get_args_val(args, default_timezone, TIMEZONE, keyname_timezone)
    hours = int(get_args_val(args, default_hours, HOURS, keyname_hours))
    daystart = get_args_val(args, default_daystart, DAYSTART, keyname_daystart)

    tzone = pytz.timezone(timezone)
    start_time = tzone.localize(parse(daystart)).time()

    dates = args.__getattribute__(DATE)
    dt_start = dates[0]
    start = tzone.localize(parse(dt_start))

    if len(dates) == 2:
        end = tzone.localize(parse(dates[1]))
        if end < start:
            raise ValueError("End date must come after start")
        if start == end:
            end = start + relativedelta(days=1)
    elif len(dates) == 1:
        end = start + relativedelta(days=1)
    else:
        raise Exception("unhandled condition")

    PROJECT_OPTION = Target.the("project option").located_by(
        By.xpath(
            f'//*[@id="select2-projectSelectManual-results"]'
            f'//li[string() = "{project}"]'
        )
    )

    ################################################################################
    client = ClockifyAPIClient().build(api, "api.clockify.me/v1")

    actor = Actor.named("user")

    day = start
    runonce = True
    ################################################################################
    while day < end:
        # skip weekends
        if day.weekday() >= 5:
            day += relativedelta(days=1)
            continue

        total_hours = get_hours_total_for_day(client, day)
        needed_hours = timedelta(hours=hours) - total_hours
        if not needed_hours:
            day += relativedelta(days=1)
            continue

        if runonce:
            driver = setup_selenium()
            actor.who_can(
                BrowseTheWeb.using(driver),
                Authenticate.with_user_pass(username, password),
                ManageBrowserLocalStorage.using(driver),
                AuthenticateWith2FA.using_secret(otp),
            )

            actor.attempts_to(LoginToJiraViaJumpCloud(url))
            actor.attempts_to(GetToJiraClockify())
            runonce = False

        actor.attempts_to(
            LogTimeInJiraClockify(day, needed_hours, start_time, PROJECT_OPTION)
        )
        day += relativedelta(days=1)
