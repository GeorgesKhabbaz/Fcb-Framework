"""Pytest configuration file for setting up browser fixtures."""

import os
import logging
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

    cfg = get_config()
    screenshots_dir_cfg = (
        cfg.get("paths", {}).get("screenshots")
        or str(Path("reports") / "screenshots")
    )
    screenshots_dir = Path(screenshots_dir_cfg)
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
        # Also attach a link to the session log file if configured
        logs_dir_cfg = cfg.get("paths", {}).get("logs")
        if logs_dir_cfg:
            log_files = sorted(Path(logs_dir_cfg).glob("*.log"))
            if log_files:
                latest_log = log_files[-1]
                extra.append(extras.html(f'<div>Session log: <a href="{latest_log.as_posix()}" target="_blank">{latest_log.name}</a></div>'))
        rep.extra = extra
    except Exception:
        # Silently ignore if pytest-html is not installed
        pass


def _configure_logging() -> Path:
    """Configure root logging to write to a timestamped file under paths.logs.

    Returns:
        Path: The path to the created log file.
    """
    cfg = get_config()
    logs_dir_cfg = (
        cfg.get("paths", {}).get("logs")
        or str(Path("reports") / "logs")
    )
    logs_dir = Path(logs_dir_cfg)
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"test_session_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.info("Logging initialized. Writing to %s", log_path)
    return log_path


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Initialize logging at the start of the test session."""
    _configure_logging()
