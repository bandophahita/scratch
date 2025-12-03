from __future__ import annotations

from typing import TYPE_CHECKING, Self

from screenpy import Actor, Answerable, UnableToAnswer, beat
from screenpy_selenium import BrowseTheWeb, Target

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class ComputedStyle(Answerable):
    target: Target | None
    element: WebElement | None

    @beat("{} examines computed style '{property}' of {target_to_log}")
    def answered_by(self, actor: Actor) -> object:
        driver = actor.ability_to(BrowseTheWeb).browser
        if not self.element:
            if not self.target:
                raise UnableToAnswer("Must supply target")
            element = self.target.found_by(actor)
        else:
            element = self.element

        return driver.execute_script(
            f"return window.getComputedStyle(arguments[0])"
            f".getPropertyValue('{self.property}')",
            element,
        )

    @property
    def target_to_log(self) -> str:
        if self.element:
            return f"{self.element.tag_name}"
        return f"{self.target}"

    def describe(self) -> str:
        """Describe the Question."""
        return f"The computed style '{self.property}' of {self.target_to_log}."

    def from_element(self, element: WebElement) -> Self:
        self.element = element
        return self

    def of_the(self, target: Target) -> Self:
        """Target the element to get the computed style property from."""
        self.target = target
        return self

    of = of_the_first_of_the = of_the

    def __init__(self, prop: str) -> None:
        self.property = prop
        self.target = None
        self.element = None


class ComputedStyleBefore(ComputedStyle):
    """Hacked version of ComputedStyle to attempt grabbing `body::before`"""

    @beat("{} examines computed style '{property}' of {target_to_log}")
    def answered_by(self, actor: Actor) -> object:
        driver = actor.ability_to(BrowseTheWeb).browser
        if not self.element:
            if not self.target:
                raise UnableToAnswer("Must supply target")
            element = self.target.found_by(actor)
        else:
            element = self.element

        return driver.execute_script(
            "return window.getComputedStyle(arguments[0], '::before')"
            # f".getPropertyValue('{self.property}')",
            ,
            element,
        )
