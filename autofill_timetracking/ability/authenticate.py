from dataclasses import dataclass

from screenpy import Actor
from screenpy.protocols import Forgettable


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

    @staticmethod
    def using(credentials: Credentials):
        return Authenticate(credentials)

    @staticmethod
    def with_user_pass(username: str, password: str):
        return Authenticate(Credentials(username, password))

    with_credentials = using

    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def forget(self):
        del self.credentials

    def to_get_credentials(self):
        return self.credentials

    def to_get_username(self):
        return self.credentials.username

    username = get_username = to_get_username

    def to_get_password(self):
        return self.credentials.password

    password = get_password = to_get_password

    @staticmethod
    def as_(actor: Actor):
        return actor.ability_to(Authenticate).to_get_credentials()

    def __repr__(self) -> str:
        return "authenticate"

    get_credentials = to_give_credentials = to_supply_credentials = to_get_credentials
