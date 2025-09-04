# Facebook Login Test Automation (Selenium + Pytest)

A lightweight, Page Object Model (POM) test framework that automates the Facebook login flow using Selenium WebDriver and Pytest.

## Features

- Page Object Model with clear separation of locators, pages, and tests
- Centralized config via YAML with secure env-var overrides
- Cross-browser support (Chrome, Firefox) with `webdriver-manager`
- Pytest fixture for driver lifecycle and auto navigation to base URL
- Automatic screenshot capture on test failures (saved under `reports/screenshots/`)
 - Automatic screenshot capture on test failures (saved under `reports/screenshots/`)
 - HTML reporting support with `pytest-html` and session logs in `reports/logs/`

## Repository Structure

```
config/
  config.yaml            # Default config (browser, base_url, paths, credentials)
  config_reader.py       # Loads YAML and applies env var overrides
locators/
  login_locators.py      # Selenium locators for the Facebook login page
pages/
  base_page.py           # Shared Selenium helpers (click, send_keys, waits)
  login_page.py          # Facebook Login page object and login flow
tests/
  test_facebook_login.py # Example test using the LoginPage
utilities/
  browser.py             # WebDriver setup (Chrome/Firefox, headless mode)
conftest.py              # Pytest fixtures & failure screenshot hook
pytest.ini               # Pytest discovery and warning filters
requirements.txt         # Pinned dependencies
reports/                 # Test artifacts (screenshots, reports)
```

## Prerequisites

- Python 3.9+
- Google Chrome or Mozilla Firefox installed

## Installation

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` as needed:

```yaml
browser: chrome                # chrome | firefox
base_url: "https://www.facebook.com/"

credentials:
  username: "your_email@test.com"
  password: "your_password"

paths:
  driver_path: "C:/drivers/chromedriver.exe"   # optional when using webdriver-manager
  screenshots: "reports/screenshots/"
  logs: "reports/logs/"
```

Sensitive values can be overridden via environment variables at runtime (preferred):

- `FB_USERNAME`
- `FB_PASSWORD`

For PowerShell (Windows):

```powershell
$env:FB_USERNAME = "my_email@example.com"
$env:FB_PASSWORD = "my_strong_password"
```

## Running Tests

From the project root:

```bash
pytest
```

Pytest configuration in `pytest.ini` sets discovery rules and quiet output. Screenshots for failed tests are saved to `reports/screenshots/` and, if `pytest-html` is installed, embedded into the HTML report.

Optional: generate an HTML report

```bash
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

## Cross-Browser and Headless

- Set `browser` in `config/config.yaml` to `chrome` or `firefox`.
- To run headless, add the following to `config/config.yaml`:

```yaml
headless: true
```

## How It Works

- `conftest.py` provides a `driver` fixture that initializes a browser via `utilities/browser.py`, opens the `base_url`, and quits after the test.
- `pages/` implement POM classes; `BasePage` wraps common actions and explicit waits.
- `locators/` centralizes selectors to minimize churn when the UI changes.
- `tests/` contain concise, readable test cases that use page objects rather than raw Selenium calls.

## Extending the Framework

- Add new page objects under `pages/` and corresponding locators under `locators/`.
- Keep tests thin: compose page methods to express scenarios.
- Reuse the `driver` fixture or add new fixtures in `conftest.py` for data setup/teardown.

## Troubleshooting

- Driver install issues: ensure internet access; `webdriver-manager` downloads drivers at runtime.
- Element not found/timeouts: verify selectors in `locators/` and adjust waits in `BasePage`.
- No screenshots or logs: ensure `reports/screenshots/` and `reports/logs/` are writable; paths can be customized in `config.yaml`.
- Authentication or 2FA prompts: when using real Facebook credentials, flows may vary; consider stubbing or using test accounts.

## License

This project is licensed under the MIT License. See `LICENSE` for details.


