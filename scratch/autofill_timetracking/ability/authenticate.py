from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from screenpy.protocols import Forgettable

if TYPE_CHECKING:
    from screenpy import Actor


@dataclass
class Credentials:
    username: str
    password: str


class Authenticate(Forgettable):
    """
    The ability to authenticate using a username and password

    "It would be a mistake to assume all actors have the ability to authenticate
    in your application"

    Example:

        George = Actor.named("George").who_can(
            Authenticate.with_credentials(credentials)
            )
    """

    @classmethod
    def using(cls, credentials: Credentials) -> Self:
        return cls(credentials)

    @classmethod
    def with_user_pass(cls, username: str, password: str) -> Self:
        return cls(Credentials(username, password))

    with_credentials = using

    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

    def forget(self) -> None:
        del self.credentials

    def to_get_credentials(self) -> Credentials:
        return self.credentials

    def to_get_username(self) -> str:
        return self.credentials.username

    username = get_username = to_get_username

    def to_get_password(self) -> str:
        return self.credentials.password

    password = get_password = to_get_password

    @classmethod
    def as_(cls, actor: Actor) -> Credentials:
        return actor.ability_to(cls).to_get_credentials()

    def __repr__(self) -> str:
        return "authenticate"

    get_credentials = to_give_credentials = to_supply_credentials = to_get_credentials


class AuthenticateGoogle(Authenticate):
    pass


class AuthenticateJumpcloud(Authenticate):
    pass
