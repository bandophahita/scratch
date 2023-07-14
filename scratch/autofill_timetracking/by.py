from __future__ import annotations

import re

from selenium.webdriver.common.by import By as _By

T = tuple[str, str]


class By(_By):
    @staticmethod
    def cls(s: str) -> T:
        return By.css(f".{s}")

    @staticmethod
    def css(s: str) -> T:
        return (By.CSS_SELECTOR, s)

    @staticmethod
    def css_attr(s: str, attrib: str) -> T:
        return By.css(f'[{attrib}="{s}"]')

    @staticmethod
    def dti(s: str) -> T:
        return By.css_attr(s, "data-testid")

    @staticmethod
    def id(s: str) -> T:  # noqa: A003
        return (By.ID, s)

    @staticmethod
    def name(s: str) -> T:
        return By.css_attr(s, "name")

    @staticmethod
    def tag(s: str) -> T:
        return (By.TAG_NAME, s)

    @staticmethod
    def xpath(s: str) -> T:
        return (By.XPATH, s)


def escape_css_selector(s: str) -> str:
    return re.sub(r"([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^`{|}~])", r"\\\g<1>", s)
