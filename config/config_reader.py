"""Utility module to load configuration settings from YAML with env overrides."""

import os
import yaml


def get_config():
    """
    Loads configuration from config.yaml and applies environment overrides.

    Returns:
        dict: Dictionary containing configuration data.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    # Environment variable overrides for sensitive data
    username = os.getenv("FB_USERNAME")
    password = os.getenv("FB_PASSWORD")
    if username:
        config.setdefault("credentials", {})["username"] = username
    if password:
        config.setdefault("credentials", {})["password"] = password

    return config
