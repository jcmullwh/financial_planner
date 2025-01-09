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
        ValueError: If the YAML file is empty or contains syntax errors.
    """
    try:
        with open(filepath) as file:
            loaded_config = yaml.safe_load(file)
            if loaded_config is None:
                error_message = "Configuration file is empty."
                raise ValueError(error_message)
            if not isinstance(loaded_config, dict):
                error_message = "Configuration must be a dictionary."
                raise ValueError(error_message)
            config = cast(dict[str, Any], loaded_config)  # Ensures type consistency
            debug_message = f"[DEBUG] Configuration loaded from {filepath}."
            print(debug_message)
            time_frequency = config.get("time_frequency", "YEAR").upper()
            if time_frequency not in {"YEAR", "MONTH", "DAY"}:
                error_message = f"Invalid time_frequency: {time_frequency}. Must be YEAR, MONTH, or DAY."
                raise ValueError(error_message)
            events = config.get("events", [])
            for event in events:
                validate_event(event)

            print("[DEBUG] Scenario loaded successfully.")
            return config
    except FileNotFoundError as e:
        message = f"Configuration file {filepath} not found."
        raise FileNotFoundError(message) from e
    except yaml.YAMLError as e:
        message = f"Error parsing YAML file: {e}"
        raise ValueError(message) from e


def validate_event(event: dict) -> None:
    """
    Validates the structure and required fields of an event.

    Args:
        event (dict): The event dictionary to validate.

    Raises:
        ValueError: If the event structure is invalid.
    """
    required_fields = ["year", "type"]
    for field in required_fields:
        if field not in event:
            error_message = f"Each event must have 'year' and 'type' fields. Invalid event: {event}"
            raise ValueError(error_message)

    event_type = event["type"]
    if event_type == "house_purchase":
        if "principal" not in event or "interest_rate" not in event:
            print(event)
            error_message = (
                f"'house_purchase' events must include 'principal' and 'interest_rate'. Invalid event: {event}"
            )
            raise ValueError(error_message)
        if event["principal"] <= 0 or event["interest_rate"] <= 0:
            error_message = "'principal' and 'interest_rate' must be positive numbers."
            raise ValueError(error_message)
    elif event_type == "new_child":
        pass  # No additional fields required currently
    elif event_type == "job_change":
        if "member_name" not in event or "new_income" not in event:
            error_message = f"Job change event must include 'member_name' and 'new_income'. Invalid event: {event}"
            raise ValueError(error_message)
        if event["new_income"] < 0:
            error_message = "'new_income' must be a non-negative number."
            raise ValueError(error_message)
    elif event_type == "windfall":
        if "amount" not in event:
            error_message = f"Windfall event must include 'amount'. Invalid event: {event}"
            raise ValueError(error_message)
        if event["amount"] < 0:
            error_message = "'amount' must be a non-negative number."
            raise ValueError(error_message)
    else:
        error_message = f"Unknown event type: {event_type}."
        raise ValueError(error_message)
