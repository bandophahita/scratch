from typing import Self

from screenpy import Actor, beat
from screenpy_selenium import Enter, Target
from selenium.webdriver import ActionChains

from scratch.autofill_timetracking.ability import (
    AuthenticateWith2FA,
    AuthenticateWith2FAGoogle,
    AuthenticateWith2FAJumpcloud,
)
from scratch.autofill_timetracking.actions import Wait
from scratch.autofill_timetracking.by import By


class Enter2FAToken:
    """
    Enter the current two-factor authentication token into an input field.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
        :external+screenpy_pyotp:class:`~screenpy_pyotp.abilities.AuthenticateWith2FA`

    Examples::

        the_actor.attempts_to(Enter2FAToken.into_the(2FA_INPUT_FIELD))
    """

    ability = AuthenticateWith2FA

    @classmethod
    def into_the(cls, target: Target) -> Self:
        """
        Target the element into which to enter the 2FA token.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Enter2FAToken.into`
        """
        return cls(target)

    @classmethod
    def into(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter2FAToken.into_the`."""
        return cls.into_the(target=target)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Enter a 2FA token into the {self.target}."

    @beat("{} enters their 2FA token into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter their 2FA token into the element."""
        token = the_actor.uses_ability_to(self.ability).to_get_token()
        the_actor.attempts_to(Enter.the_text(token).into_the(self.target))

    @beat("Enter their 2FA token into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Enter2FAToken Action to a Chain of Actions."""
        token = the_actor.uses_ability_to(self.ability).to_get_token()
        the_chain.send_keys_to_element(self.target.found_by(the_actor), token)

    def __init__(self, target: Target) -> None:
        self.target = target


class EnterGoogle2FAToken(Enter2FAToken):
    ability = AuthenticateWith2FAGoogle


class EnterJumpcloud2FAToken(Enter2FAToken):
    ability = AuthenticateWith2FAJumpcloud

    @beat("{} enters their 2FA token into the {target}.")
    def perform_as(self, actor: Actor) -> None:
        """Direct the Actor to enter their 2FA token into the element."""
        token = actor.uses_ability_to(self.ability).to_get_token()
        # actor.attempts_to(Enter.the_text(token).into_the(self.target))

        TOKEN_1 = Target("token 1").located(By.xpath("(//input[@type='text'])[1]"))
        TOKEN_2 = Target("token 2").located(By.xpath("(//input[@type='text'])[2]"))
        TOKEN_3 = Target("token 3").located(By.xpath("(//input[@type='text'])[3]"))
        TOKEN_4 = Target("token 4").located(By.xpath("(//input[@type='text'])[4]"))
        TOKEN_5 = Target("token 5").located(By.xpath("(//input[@type='text'])[5]"))
        TOKEN_6 = Target("token 6").located(By.xpath("(//input[@type='text'])[6]"))

        t1 = token[0]
        t2 = token[1]
        t3 = token[2]
        t4 = token[3]
        t5 = token[4]
        t6 = token[5]

        actor.will(Wait.for_(TOKEN_1).to_appear())
        actor.will(Enter(t1).into(TOKEN_1))
        actor.will(Enter(t2).into(TOKEN_2))
        actor.will(Enter(t3).into(TOKEN_3))
        actor.will(Enter(t4).into(TOKEN_4))
        actor.will(Enter(t5).into(TOKEN_5))
        actor.will(Enter(t6).into(TOKEN_6))
