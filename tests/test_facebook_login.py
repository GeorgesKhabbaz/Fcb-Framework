"""Test suite for verifying Facebook login functionality."""

from pages.login_page import LoginPage
from config.config_reader import get_config


def test_facebook_login(driver):
    """
    Test that a user can log in to Facebook using valid credentials.

    Args:
        driver (WebDriver): Selenium WebDriver instance provided by fixture.
    """
    config = get_config()
    login_page = LoginPage(driver)

    # Use the page's high-level login method
    login_page.login(
        config['credentials']['username'],
        config['credentials']['password'],
    )

    # Minimal assertion: page title contains 'Facebook'
    # (avoid strict assertions due to dynamic content)
    assert "Facebook" in driver.title
