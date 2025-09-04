"""Utility module to initialize and configure different browsers for Selenium tests."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config_reader import get_config


def setup_browser():
    """
    Initializes the Selenium WebDriver based on the browser and options from config.

    Returns:
        WebDriver: Selenium WebDriver instance.

    Raises:
        ValueError: If the browser type is not supported.
    """
    cfg = get_config()
    browser_type = cfg.get("browser", "chrome").lower()
    headless = cfg.get("headless", False)

    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1366,768")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
        return driver
    elif browser_type == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        driver.set_window_size(1366, 768)
        return driver
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")
