from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.actions import Eventually, SeeAnyOf
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy_pyotp.abilities import AuthenticateWith2FA
from screenpy_selenium import Enter, Target
from screenpy_selenium.actions import Click, Enter2FAToken, Open, Wait
from screenpy_selenium.questions import Element
from screenpy_selenium.resolutions import IsClickable

from ..by import By
from . import EnterPassword, EnterUsername

if TYPE_CHECKING:
    from screenpy import Actor

CONTINUE_WITH_GOOGLE_BUTTON = Target.the("Continue with google button").located_by(
    By.id("google-auth-button")
)
LOGIN_FIELD = Target.the("google login email field").located_by(By.id("identifierId"))
NEXT_BUTTON = Target.the("email_next_button").located_by(
    By.xpath('//button[contains(string(), "Next")]')
)
PASSWORD_FIELD = Target.the("password field").located_by((By.NAME, "Passwd"))
TOTP_PIN_FIELD = Target.the("TOTP PIN field").located_by(By.id("totpPin"))
TRY_ANOTHER_WAY_BUTTON = Target.the("try another way button").located_by(
    By.xpath('//button[contains(string(), "Try another way")]')
)
CODE_FROM_AUTHENTICATOR_BUTTON = Target.the(
    "code from authenticator button"
).located_by(
    By.xpath('//div[@role="link"][contains(string(), "Google Authenticator")]')
)
PROGRESS_BAR = Target("progress bar").located('//*[@role="progressbar"]')

USERNAME_FIELD = Target("username_field").located(By.id("username"))

LOGIN_SUBMIT_BUTTON = Target("login submit").located(By.id("login-submit"))

JUMPCLOUD_USERNAME = Target("jumpcloud_username").located(
    By.xpath("//input[@placeholder='User Email Address']")
)
JUMPCLOUD_CONTINUE = Target("jumpcloud continue").located(
    By.xpath("//button[@type='submit']")
)
JUMPCLOUD_PASSWORD = Target("jumpcloud password").located(
    By.xpath("//input[@placeholder='Password']")
)


TOKEN_1 = Target("token 1").located(By.xpath("(//input[@type='text'])[1]"))

TOKEN_2 = Target("token 2").located(By.xpath("(//input[@type='text'])[2]"))

TOKEN_3 = Target("token 3").located(By.xpath("(//input[@type='text'])[3]"))

TOKEN_4 = Target("token 4").located(By.xpath("(//input[@type='text'])[4]"))

TOKEN_5 = Target("token 5").located(By.xpath("(//input[@type='text'])[5]"))

TOKEN_6 = Target("token 6").located(By.xpath("(//input[@type='text'])[6]"))


class LoginToJiraViaGoogle(Performable):
    @beat("[TASK] {} attempts to LoginToJiraViaGoogle")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Open(self.url))
        actor.will(Wait.for_the(CONTINUE_WITH_GOOGLE_BUTTON).to_be_clickable())
        actor.will(Eventually(Click(CONTINUE_WITH_GOOGLE_BUTTON)))

        actor.will(Eventually(EnterUsername.into_the(LOGIN_FIELD)))
        actor.will(Wait.for_the(NEXT_BUTTON).to_be_clickable())
        actor.will(Eventually(Click(NEXT_BUTTON)))
        actor.will(Wait.for_(PROGRESS_BAR).to_disappear())

        actor.will(Eventually(EnterPassword.into_the(PASSWORD_FIELD)))
        actor.will(Wait.for_the(NEXT_BUTTON).to_be_clickable())
        actor.will(Eventually(Click(NEXT_BUTTON)))

        actor.should(
            Eventually(
                SeeAnyOf(
                    (Element(TOTP_PIN_FIELD), IsClickable()),
                    (Element(TRY_ANOTHER_WAY_BUTTON), IsClickable()),
                )
            )
        )

        if not Element(TOTP_PIN_FIELD).answered_by(actor):
            actor.should(Eventually(Click(TRY_ANOTHER_WAY_BUTTON)))
            actor.should(Eventually(Click(CODE_FROM_AUTHENTICATOR_BUTTON)))

        actor.will(
            Eventually(Enter2FAToken.into_the(TOTP_PIN_FIELD)),
            Eventually(Click(NEXT_BUTTON)),
        )
        return

    @staticmethod
    def using(url: str) -> LoginToJiraViaGoogle:
        return LoginToJiraViaGoogle(url)

    def __init__(self, url: str):
        self.url = url


class LoginToJiraViaJumpCloud(Performable):
    @beat("[TASK] {} attempts to LoginToJiraViaJumpCloud")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Open(self.url))
        # clockify username
        actor.will(Eventually(EnterUsername.into_the(USERNAME_FIELD)))
        actor.will(Eventually(Click(LOGIN_SUBMIT_BUTTON)))
        actor.will(Wait.for_(JUMPCLOUD_USERNAME).to_appear())

        # jumpcloud username
        actor.will(Eventually(EnterUsername.into_the(JUMPCLOUD_USERNAME)))
        actor.will(Click(JUMPCLOUD_CONTINUE))

        actor.will(Eventually(EnterPassword.into_the(JUMPCLOUD_PASSWORD)))
        actor.will(Click(JUMPCLOUD_CONTINUE))

        token = actor.uses_ability_to(AuthenticateWith2FA).to_get_token()

        t1, t2, t3, t4, t5, t6 = token
        actor.will(Wait.for_(TOKEN_1).to_appear())
        actor.will(Enter(t1).into(TOKEN_1))
        actor.will(Enter(t2).into(TOKEN_2))
        actor.will(Enter(t3).into(TOKEN_3))
        actor.will(Enter(t4).into(TOKEN_4))
        actor.will(Enter(t5).into(TOKEN_5))
        actor.will(Enter(t6).into(TOKEN_6))

        return

    @staticmethod
    def using(url: str) -> LoginToJiraViaGoogle:
        return LoginToJiraViaGoogle(url)

    def __init__(self, url: str):
        self.url = url
