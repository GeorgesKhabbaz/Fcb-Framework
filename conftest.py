"""Pytest configuration file for setting up browser fixtures."""

import os
from datetime import datetime
from pathlib import Path
import pytest
from utilities.browser import setup_browser
from config.config_reader import get_config


@pytest.fixture
def driver():
    """
    Pytest fixture to initialize and quit the browser.

    Yields:
        WebDriver: Selenium WebDriver instance.
    """
    browser = setup_browser()
    # Navigate to base URL before yielding driver
    base_url = get_config().get("base_url")
    if base_url:
        browser.get(base_url)
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails and attach to HTML report if enabled."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or rep.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    screenshots_dir = Path("reports") / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{item.name}_{timestamp}.png"
    file_path = screenshots_dir / file_name

    try:
        driver.save_screenshot(str(file_path))
    except Exception:
        return

    # Attach to pytest-html report if the plugin is installed
    try:
        from pytest_html import extras  # type: ignore

        extra = getattr(rep, "extra", [])
        extra.append(extras.png(str(file_path)))
        rep.extra = extra
    except Exception:
        # Silently ignore if pytest-html is not installed
        pass
