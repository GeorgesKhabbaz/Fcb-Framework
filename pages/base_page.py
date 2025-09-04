"""Base page class containing common Selenium actions."""

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class for all page objects with common Selenium utilities."""

    def __init__(self, driver):
        """
        Initialize the BasePage with a WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        """
        Wait for element to be clickable and perform a click.

        Args:
            locator (tuple): Locator strategy and value (By, locator).
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        """
        Wait for element to be present and send input text.

        Args:
            locator (tuple): Locator strategy and value (By, locator).
            text (str): The text to type into the element.
        """
        self.wait.until(EC.presence_of_element_located(locator)).send_keys(text)

    def get_title(self):
        """
        Get the current page title.

        Returns:
            str: The title of the current page.
        """
        return self.driver.title
