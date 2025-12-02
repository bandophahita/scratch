from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import Silently
from screenpy.actions import Eventually, SeeAnyOf
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy_selenium import Enter, Target
from screenpy_selenium.actions import Click, Open, Wait
from screenpy_selenium.questions import Element
from screenpy_selenium.resolutions import IsClickable

from scratch.autofill_timetracking.ability import (
    AuthenticateGoogle,
    AuthenticateJumpcloud,
    AuthenticateWith2FAJumpcloud,
)
from scratch.autofill_timetracking.actions import (
    EnterGoogle2FAToken,
    EnterPassword,
    EnterUsername,
)
from scratch.autofill_timetracking.by import By

if TYPE_CHECKING:
    from screenpy import Actor

CONTINUE_WITH_GOOGLE_BUTTON = Target.the("Continue with google button").located_by(
    By.id("google-auth-button")
)
JIRA_EMAIL = Target("Jira Email").located(By.id("username-uid1"))
JIRA_LOGIN_SUBMIT_CONTINUE = Target("Jira Login Submit (Continue)").located(
    By.id("login-submit")
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
    By.xpath("//input[@placeholder='User Password']")
)


TOKEN_1 = Target("token 1").located(By.xpath("(//input[@type='text'])[1]"))

TOKEN_2 = Target("token 2").located(By.xpath("(//input[@type='text'])[2]"))

TOKEN_3 = Target("token 3").located(By.xpath("(//input[@type='text'])[3]"))

TOKEN_4 = Target("token 4").located(By.xpath("(//input[@type='text'])[4]"))

TOKEN_5 = Target("token 5").located(By.xpath("(//input[@type='text'])[5]"))

TOKEN_6 = Target("token 6").located(By.xpath("(//input[@type='text'])[6]"))


class LoginToJiraViaGoogle(Performable):
    @beat("[TASK] {} tries to LoginToJiraViaGoogle")
    def perform_as(self, actor: Actor) -> None:
        google_password = AuthenticateGoogle.as_(actor).password
        google_username = AuthenticateGoogle.as_(actor).username

        actor.will(Open(self.url))
        actor.will(Wait.for_the(CONTINUE_WITH_GOOGLE_BUTTON).to_be_clickable())
        actor.will(Eventually(Click(CONTINUE_WITH_GOOGLE_BUTTON)))

        actor.will(Enter(google_username).into_the(LOGIN_FIELD))
        # actor.will(Wait.for_the(NEXT_BUTTON).to_be_clickable())
        actor.will(Eventually(Click(NEXT_BUTTON)))
        actor.will(Wait.for_(PROGRESS_BAR).to_disappear())
        actor.will(Wait.for_(PASSWORD_FIELD).to_be_clickable())

        actor.will(
            Eventually(Enter.the_secret(google_password).into_the(PASSWORD_FIELD))
        )
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
            Eventually(EnterGoogle2FAToken.into_the(TOTP_PIN_FIELD)),
            Eventually(Click(NEXT_BUTTON)),
        )

        # next we need to login via jumpcloud
        actor.will(StepsToLoginToJiraViaJumpCloud())

    @staticmethod
    def using(url: str) -> LoginToJiraViaGoogle:
        return LoginToJiraViaGoogle(url)

    def __init__(self, url: str):
        self.url = url


class StepsToLoginToJiraViaJumpCloud(Performable):
    def perform_as(self, actor: Actor) -> None:
        jc_password = AuthenticateJumpcloud.as_(actor).password
        jc_username = AuthenticateJumpcloud.as_(actor).username

        # jumpcloud username
        actor.will(Silently(Wait.for_(JUMPCLOUD_USERNAME).to_appear()))
        actor.will(Enter(jc_username).into_the(JUMPCLOUD_USERNAME))
        actor.will(Click(JUMPCLOUD_CONTINUE))
        actor.will(Silently(Wait.for_(JUMPCLOUD_PASSWORD).to_appear()))
        actor.will(Enter.the_secret(jc_password).into_the(JUMPCLOUD_PASSWORD))
        actor.will(Click(JUMPCLOUD_CONTINUE))

        token = actor.uses_ability_to(AuthenticateWith2FAJumpcloud).to_get_token()

        # t1, t2, t3, t4, t5, t6 = token
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


class LoginToJiraViaJumpCloud(Performable):
    @beat("[TASK] {} tries to LoginToJiraViaJumpCloud")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Open(self.url))
        # clockify username
        actor.will(Silently(Wait.for_(USERNAME_FIELD).to_appear()))
        actor.will(EnterUsername.into_the(USERNAME_FIELD))
        actor.will(Click(LOGIN_SUBMIT_BUTTON))
        actor.will(Silently(Wait.for_(JUMPCLOUD_USERNAME).to_appear()))

        # jumpcloud username
        actor.will(StepsToLoginToJiraViaJumpCloud())

    @staticmethod
    def using(url: str) -> LoginToJiraViaJumpCloud:
        return LoginToJiraViaJumpCloud(url)

    def __init__(self, url: str):
        self.url = url
