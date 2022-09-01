from __future__ import annotations

from screenpy import Actor
from screenpy.actions import Eventually, SeeAnyOf
from screenpy.pacing import beat
from screenpy.protocols import Performable
from screenpy_selenium import Target
from screenpy_selenium.actions import Click, Enter2FAToken, Open
from screenpy_selenium.questions import Element
from screenpy_selenium.resolutions import IsClickable
from selenium.webdriver.common.by import By

from autofill_timetracking.actions import EnterPassword, EnterUsername

# @formatter:off
# fmt: off
CONTINUE_WITH_GOOGLE_BUTTON = Target.the(
    f"Continue with google button").located_by((
        By.ID,
        "google-auth-button"
        ))
LOGIN_FIELD = Target.the(
    f"google login email field").located_by((
        By.ID,
        'identifierId'
        ))
NEXT_BUTTON = Target.the(
    f"email_next_button").located_by((
        By.XPATH,
        '//button[contains(string(), "Next")]'
        ))
PASSWORD_FIELD = Target.the(
    f"password field").located_by((
        By.NAME,
        'password'
        ))
TOTP_PIN_FIELD = Target.the(
    f"TOTP PIN field").located_by((
        By.ID,
        'totpPin'
        ))
TRY_ANOTHER_WAY_BUTTON = Target.the(
    f"try another way button").located_by((
        By.XPATH,
        '//button[contains(string(), "Try another way")]'
        ))
CODE_FROM_AUTHENTICATOR_BUTTON = Target.the(
    f"code from authenticator button").located_by((
        By.XPATH,
        '//div[@role="link"][contains(string(), "Google Authenticator")]'
        ))
# fmt: on
# @formatter:on


class LoginToJira(Performable):
    @beat("[TASK] {} attempts to LoginToJira")
    def perform_as(self, actor: Actor):
        actor.attempts_to(Open(self.url))
        actor.attempts_to(Eventually(Click(CONTINUE_WITH_GOOGLE_BUTTON)))
        actor.attempts_to(
            Eventually(EnterUsername.into_the(LOGIN_FIELD)),
            Eventually(Click(NEXT_BUTTON)),
        )
        actor.attempts_to(
            Eventually(EnterPassword.into_the(PASSWORD_FIELD)),
            Eventually(Click(NEXT_BUTTON)),
        )

        actor.should(
            Eventually(
                SeeAnyOf(
                    (Element(TOTP_PIN_FIELD), IsClickable()),
                    (Element(TRY_ANOTHER_WAY_BUTTON), IsClickable()),
                )
            )
        )

        if Element(TRY_ANOTHER_WAY_BUTTON).answered_by(actor):
            actor.should(Eventually(Click(TRY_ANOTHER_WAY_BUTTON)))
            actor.should(Eventually(Click(CODE_FROM_AUTHENTICATOR_BUTTON)))

        actor.attempts_to(
            Eventually(Enter2FAToken.into_the(TOTP_PIN_FIELD)),
            Click(NEXT_BUTTON),
        )
        return

    @staticmethod
    def using(url: str):
        return LoginToJira(url)

    def __init__(self, url: str):
        self.url = url
