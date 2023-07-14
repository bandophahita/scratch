"""
Enter a 2-factor authentication code into a text field.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat
from screenpy_selenium.actions import Enter

from ..ability import Authenticate

if TYPE_CHECKING:
    from screenpy.actor import Actor
    from screenpy_selenium import Target
    from selenium.webdriver.common.action_chains import ActionChains


class EnterUsername:
    """Enter the username into an input field.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
        :external+screenpy_pyotp:class:`~autofill_timetracking.ability.Authenticate`

    Examples::

        the_actor.attempts_to(EnterUsername.into_the(USERNAME_FIELD))
    """

    @staticmethod
    def into_the(target: Target) -> EnterUsername:
        """Target the element into which to enter the username"""
        return EnterUsername(target)

    into = into_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Enter username into the {self.target}."

    @beat("{} enters their username into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter their username into the element."""
        username = the_actor.uses_ability_to(Authenticate).to_get_username()
        the_actor.attempts_to(Enter.the_text(username).into_the(self.target))

    @beat("  Enter their username into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the EnterUsername Action to a Chain of Actions."""
        username = the_actor.uses_ability_to(Authenticate).to_get_username()
        the_chain.send_keys_to_element(self.target.found_by(the_actor), username)

    def __init__(self, target: Target) -> None:
        self.target = target


class EnterPassword:
    """Enter the password into an input field.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
        :external+screenpy_pyotp:class:`~autofill_timetracking.ability.Authenticate`

    Examples::

        the_actor.attempts_to(EnterPassword.into_the(USERNAME_FIELD))
    """

    @staticmethod
    def into_the(target: Target) -> EnterPassword:
        """Target the element into which to enter the password"""
        return EnterPassword(target)

    into = into_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Enter password into the {self.target}."

    @beat("{} enters their password into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter their password into the element."""
        password = the_actor.uses_ability_to(Authenticate).to_get_password()
        the_actor.attempts_to(Enter.the_secret(password).into_the(self.target))

    @beat("  Enter their password into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the EnterPassword Action to a Chain of Actions."""
        password = the_actor.uses_ability_to(Authenticate).to_get_password()
        the_chain.send_keys_to_element(self.target.found_by(the_actor), password)

    def __init__(self, target: Target) -> None:
        self.target = target
