from __future__ import annotations

from typing import TYPE_CHECKING, Self

from screenpy import Actor, Quietly, beat
from screenpy_selenium.abilities import BrowseTheWeb

from scratch.autofill_timetracking.actions.wait_for_animation import WaitforAnimation

if TYPE_CHECKING:
    from screenpy_selenium import Target


class ScrollIntoView:
    """https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView"""

    @beat("{} tries to ScrollIntoView {behavior}ly, {target}")
    def perform_as(self, actor: Actor) -> None:
        elem = self.target.found_by(actor)
        driver = actor.ability_to(BrowseTheWeb).browser
        driver.execute_script(
            f"arguments[0].scrollIntoView({{"
            f'block: "{self.block}", '
            f'inline: "{self.inline}", '
            f'behavior: "{self.behavior}"'
            f"}});",
            elem,
        )
        actor.will(Quietly(WaitforAnimation(self.target, self.delay)))

    def instantly(self) -> Self:
        self.behavior = "instant"
        self.delay = 0
        return self

    def smoothly(self) -> Self:
        """scrolling breaks if called with smooth while animations are disabled."""
        self.behavior = "smooth"
        self.delay = 50
        return self

    def to(self, align: str) -> Self:
        """start, center, end, nearest"""
        self.block = align
        self.inline = align
        return self

    def to_start(self) -> Self:
        return self.to("start")

    def to_center(self) -> Self:
        return self.to("center")

    def to_end(self) -> Self:
        return self.to("end")

    def to_nearest(self) -> Self:
        return self.to("nearest")

    def block_start(self) -> Self:
        self.block = "start"
        return self

    def block_end(self) -> Self:
        self.block = "end"
        return self

    def block_center(self) -> Self:
        self.block = "center"
        return self

    def block_nearest(self) -> Self:
        self.block = "nearest"
        return self

    def inline_start(self) -> Self:
        self.inline = "start"
        return self

    def inline_end(self) -> Self:
        self.inline = "end"
        return self

    def inline_center(self) -> Self:
        self.inline = "center"
        return self

    def inline_nearest(self) -> Self:
        self.inline = "nearest"
        return self

    def __init__(self, target: Target) -> None:
        self.target = target
        self.behavior = "instant"
        self.block = "start"
        self.inline = "start"
        # self.inline = "nearest"
        self.delay = 0
