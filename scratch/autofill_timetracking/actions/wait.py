from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Self

from screenpy import Actor, Quietly, settings
from screenpy_selenium import Target, Wait as _Wait
from selenium.webdriver.support import expected_conditions as EC

from .custom_expected_conditions import (
    element_located_to_be_stationary,
    element_located_to_move,
    element_to_be_enabled,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from selenium.webdriver.remote.webelement import WebElement


class Wait(_Wait):
    def to_stop_moving(self) -> Self:
        """Use Selenium's "invisibility of element located" strategy."""
        return self.using(element_located_to_be_stationary, "for {0} to stop moving...")

    def to_move(self) -> Self:
        return self.using(element_located_to_move, "for {0} to move...")

    def to_be_stale(self, log_element: str = "element") -> Self:
        return self.using(EC.staleness_of, f"for {log_element} to be stale...")

    def to_be_present(self) -> Self:
        return self.using(EC.presence_of_element_located, "for {0} to be present...")

    def to_be_enabled(self) -> Self:
        return self.using(element_to_be_enabled, "for {0} to be enabled...")

    # override original until we can fix their type hinting.
    @classmethod
    def for_the(cls, target: Target | WebElement) -> Self:
        return cls(seconds=settings.TIMEOUT, args=[target])

    @classmethod
    def for_(cls, target: Target | WebElement) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Wait.for_the`."""
        return cls.for_the(target=target)


@contextmanager
def wait_until_stale(
    actor: Actor, target: Target, timeout: float | None = None
) -> Generator[None, None, None]:
    timeout = settings.TIMEOUT if timeout is None else timeout
    elem = target.found_by(actor)
    yield
    actor.will(Quietly(Wait(timeout).for_(elem).to_be_stale(log_element=f"{target}")))


@contextmanager
def wait_until_moved(
    actor: Actor, target: Target, timeout: float | None = None
) -> Generator[None, None, None]:
    timeout = settings.TIMEOUT if timeout is None else timeout
    elem = target.found_by(actor)
    yield
    actor.will(Quietly(Wait(timeout, args=[elem, elem.rect]).to_move()))
