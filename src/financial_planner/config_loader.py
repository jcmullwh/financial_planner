# financial_planner/config_loader.py

from typing import Dict

import yaml


def load_yaml_config(filepath: str) -> Dict:
    """
    Loads and parses a YAML configuration file.

    Args:
        filepath (str): The path to the YAML configuration file.

    Returns:
        Dict: The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the YAML file contains syntax errors.
    """
    try:
        with open(filepath) as file:
            config = yaml.safe_load(file)
            print(f"[DEBUG] Configuration loaded from {filepath}.")
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {filepath} not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")
