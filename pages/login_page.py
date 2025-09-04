"""Page Object Model for Facebook login page."""

from pages.base_page import BasePage
from locators.login_locators import EMAIL_INPUT, PASSWORD_INPUT, LOGIN_BUTTON


class LoginPage(BasePage):
    """Page Object for interacting with the Facebook login page."""

    def enter_email(self, email: str):
        """Enter the email into the email input field."""
        self.send_keys(EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Enter the password into the password input field."""
        self.send_keys(PASSWORD_INPUT, password)

    def click_login(self):
        """Click on the login button."""
        self.click(LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """Perform a full login flow with provided credentials."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
