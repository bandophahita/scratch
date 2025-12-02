from __future__ import annotations

from typing import Self

from screenpy import Actor, Performable, beat, settings, the_narrator
from screenpy.speech_tools import get_additive_description


class Conditionally(Performable):
    if_action: Performable
    then_action: Performable
    else_action: Performable | None = None
    if_action_to_log: str = ""
    then_action_to_log: str = ""
    else_action_to_log: str = ""

    @beat(
        "{} tries to Conditionally '{then_action_to_log}' if '{if_action_to_log}' "
        "is True {else_action_to_log}"
    )
    def perform_as(self, actor: Actor) -> None:
        with the_narrator.mic_cable_kinked():
            if self.successful(actor, self.if_action):
                actor.will(self.then_action)
            elif self.else_action:
                if not settings.UNABRIDGED_NARRATION:
                    the_narrator.clear_backup()
                actor.will(self.else_action)
            elif not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()

    def if_(self, if_action: Performable) -> Self:
        self.if_action = if_action
        self.if_action_to_log = get_additive_description(self.if_action)
        return self

    def else_(self, else_action3: Performable) -> Self:
        self.else_action = else_action3
        self.else_action_to_log = f"else '{get_additive_description(self.else_action)}'"
        return self

    def ignoring(self, *ignored_exceptions: type[BaseException]) -> Self:
        """Set the expception classes to Ignore"""
        self.ignore_exceptions = ignored_exceptions
        return self

    def successful(self, actor: Actor, action: Performable) -> bool:
        try:
            actor.perform(action)
        except self.ignore_exceptions:
            return False
        return True

    def __init__(self, then_action: Performable) -> None:
        self.then_action = then_action
        self.then_action_to_log = get_additive_description(self.then_action)
        self.ignore_exceptions = (AssertionError,)
