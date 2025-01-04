# financial_planner/config_loader.py

from typing import Any, cast  # Added to resolve type issues

import yaml


def load_yaml_config(filepath: str) -> dict[str, Any]:
    """
    Loads and parses a YAML configuration file.

    Args:
        filepath (str): The path to the YAML configuration file.

    Returns:
        dict[str, Any]: The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the YAML file contains syntax errors.
    """
    try:
        with open(filepath) as file:
            config = cast(dict[str, Any], yaml.safe_load(file))  # Cast to dict[str, Any]
            print(f"[DEBUG] Configuration loaded from {filepath}.")
            return config
    except FileNotFoundError as e:
        message = f"Configuration file {filepath} not found."
        raise FileNotFoundError(message) from e
    except yaml.YAMLError as e:
        message = f"Error parsing YAML file: {e}"
        raise ValueError(message) from e
