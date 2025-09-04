"""Locators for Facebook login page elements."""

from selenium.webdriver.common.by import By

EMAIL_INPUT = (By.XPATH, '//*[@id="email"]')
PASSWORD_INPUT = (By.XPATH, '//*[@id="pass"]')
LOGIN_BUTTON = (By.XPATH, '//*[@name="login"]')
