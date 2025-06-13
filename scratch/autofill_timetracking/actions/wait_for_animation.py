from typing import Self

from screenpy import Actor, Quietly, beat
from screenpy_selenium import Pause, Target

from scratch.autofill_timetracking.actions.wait import Wait


class WaitforAnimation:
    @beat("{} waits for {target} animation to finish")
    def perform_as(self, actor: Actor) -> None:
        if self.delay:
            actor.will(
                Quietly(Pause(self.delay).milliseconds_because("animation start delay"))
            )
        actor.will(Quietly(Wait(1).second_for(self.target).to_stop_moving()))
        # for now, we need to wait longer here until we separate animation from loading

    @classmethod
    def of(cls, target: Target) -> Self:
        return cls(target=target)

    def delaying(self, delay: int = 0) -> Self:
        self.delay = delay
        return self

    def __init__(self, target: Target, delay: int = 50) -> None:
        self.delay = delay
        self.target = target
