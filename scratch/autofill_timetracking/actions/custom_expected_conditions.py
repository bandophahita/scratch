from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Literal

from selenium.common import InvalidSelectorException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from collections.abc import Callable

    from selenium.webdriver.remote.webdriver import WebDriver

    Loc = tuple[str, str]
    WebDriverOrWebElement = WebDriver | WebElement


def element_located_to_be_stationary(
    locator: Loc,
) -> Callable[[WebDriverOrWebElement], WebElement | Literal[False]]:
    last_position1: dict | None = None
    last_position2: dict | None = None

    def _predicate(driver: WebDriverOrWebElement) -> WebElement | Literal[False]:
        nonlocal last_position1
        nonlocal last_position2
        try:
            elem = driver.find_element(*locator)
            sleep(0.005)
            current_position = elem.rect
        except InvalidSelectorException:
            raise
        except WebDriverException:
            return False

        if last_position1 is None:
            last_position1 = current_position
            return False

        if last_position2 is None:
            last_position2 = current_position
            return False

        if (
            last_position1 != last_position2
            or last_position1 != current_position
            or last_position2 != current_position
        ):
            last_position1 = last_position2
            last_position2 = current_position
            return False
        return elem

    return _predicate


def element_located_to_move(
    locator: Loc, last_position: dict | None = None
) -> Callable[[WebDriverOrWebElement], WebElement | Literal[False]]:

    def _predicate(driver: WebDriverOrWebElement) -> WebElement | Literal[False]:
        nonlocal last_position
        try:
            elem = driver.find_element(*locator)
            sleep(0.005)
            current_position = elem.rect
        except InvalidSelectorException:
            raise
        except WebDriverException:
            return False

        if last_position is None:
            last_position = current_position
            return False

        if last_position == current_position:
            return False

        return elem

    return _predicate


def element_to_be_enabled(
    mark: WebElement | tuple[str, str],
) -> Callable[[WebDriverOrWebElement], Literal[False] | WebElement]:
    def _predicate(driver: WebDriverOrWebElement) -> Literal[False] | WebElement:
        target = mark
        if not isinstance(target, WebElement):  # if given locator instead of WebElement
            target = driver.find_element(*target)  # grab element at locator
        return _element_if_enabled(target)

    return _predicate


def enabled_element(
    element: WebElement,
) -> Callable[[WebDriverOrWebElement], Literal[False] | WebElement]:
    def _predicate(_: WebDriverOrWebElement) -> Literal[False] | WebElement:
        return _element_if_enabled(element)

    return _predicate


def _element_if_enabled(
    element: WebElement, enabled: bool = True
) -> Literal[False] | WebElement:
    return element if element.is_enabled() == enabled else False


# def is_element_animated(self, selector):
#     return self._driver.execute_script(
#         "return jQuery('" + selector + "').is(':animated');"
#     )
#
