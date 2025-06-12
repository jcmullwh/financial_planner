# financial_planner/config_loader.py

from typing import Any, Optional, cast

import yaml


def load_yaml_config(filepath: str) -> Optional[dict[str, Any]]:
    """
    Loads and parses a YAML configuration file.

    Args:
        filepath (str): The path to the YAML configuration file.

    Returns:
        Optional[dict[str, Any]]: The parsed configuration as a dictionary or None if the file is empty.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the YAML file contains syntax errors.
    """
    try:
        with open(filepath) as file:
            loaded = yaml.safe_load(file)
            print(f"[DEBUG] Configuration loaded from {filepath}.")
            return cast(Optional[dict[str, Any]], loaded)
    except FileNotFoundError as e:
        message = f"Configuration file {filepath} not found."
        raise FileNotFoundError(message) from e
    except yaml.YAMLError as e:
        message = f"Error parsing YAML file: {e}"
        raise ValueError(message) from e
