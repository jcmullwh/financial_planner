# tests/test_config_loader.py

import os
import tempfile

import pytest

from financial_planner.config_loader import load_yaml_config


def test_load_yaml_config_success():
    yaml_content = """
    start_year: 2024
    end_year: 2034
    inflation_rate: 0.02
    household:
      living_costs: 50000
      housing_costs: 20000
      members:
        - name: "Jason"
          income: 80000
          tax_rate: 0.25
        - name: "Linda"
          income: 60000
          tax_rate: 0.20
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(yaml_content)
        tmp_path = tmp.name

    try:
        config = load_yaml_config(tmp_path)
        assert config["start_year"] == 2024
        assert config["end_year"] == 2034
        assert config["inflation_rate"] == 0.02
        assert config["household"]["living_costs"] == 50000
    finally:
        os.remove(tmp_path)


def test_load_yaml_config_file_not_found():
    with pytest.raises(FileNotFoundError, match="Configuration file .* not found."):
        load_yaml_config("non_existent_file.yaml")


def test_load_yaml_config_invalid_yaml():
    invalid_yaml_content = """
    start_year: 2024
    end_year: 2034
    inflation_rate: 0.02
    household
      living_costs: 50000
      housing_costs: 20000
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(invalid_yaml_content)
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="Error parsing YAML file:"):
            load_yaml_config(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_yaml_config_empty_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="Configuration file is empty."):
            load_yaml_config(tmp_path)
    finally:
        os.remove(tmp_path)


# New Tests for Phase 2


def test_load_yaml_config_with_events():
    yaml_content = """
    start_year: 2025
    end_year: 2030
    inflation_rate: 0.03
    time_frequency: "YEAR"
    household:
      living_costs: 60000
      housing_costs: 25000
      members:
        - name: "Alice"
          income: 90000
          tax_rate: 0.25
          savings: 15000
        - name: "Bob"
          income: 70000
          tax_rate: 0.20
          savings: 10000
    events:
      - year: 2025
        type: "house_purchase"
        principal: 350000
        interest_rate: 0.035
      - year: 2027
        type: "new_child"
      - year: 2029
        type: "job_change"
        member_name: "Alice"
        new_income: 95000
      - year: 2030
        type: "windfall"
        amount: 60000
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(yaml_content)
        tmp_path = tmp.name

    try:
        config = load_yaml_config(tmp_path)
        assert config["events"] is not None
        assert len(config["events"]) == 4
        assert config["events"][0]["type"] == "house_purchase"
        assert config["events"][1]["type"] == "new_child"
        assert config["events"][2]["type"] == "job_change"
        assert config["events"][3]["type"] == "windfall"
    finally:
        os.remove(tmp_path)


def test_load_yaml_config_invalid_events_missing_fields():
    yaml_content = """
    start_year: 2025
    end_year: 2030
    household:
      living_costs: 60000
      housing_costs: 25000
      members:
        - name: "Alice"
          income: 90000
          tax_rate: 0.25
    events:
      - year: 2025
        type: "house_purchase"
        principal: 350000
        # Missing 'interest_rate'
      - year: 2027
        type: "job_change"
        # Missing 'member_name' and 'new_income'
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(yaml_content)
        tmp_path = tmp.name

    try:
        with pytest.raises(
            ValueError,
            match=(
                "'house_purchase' events must include 'principal' and 'interest_rate'. "
                "Invalid event: {'year': 2025, 'type': 'house_purchase', 'principal': 350000}"
            ),
        ):
            load_yaml_config(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_yaml_config_invalid_time_frequency():
    yaml_content = """
    start_year: 2025
    end_year: 2030
    time_frequency: "FORTNIGHT"
    household:
      living_costs: 60000
      housing_costs: 25000
      members:
        - name: "Alice"
          income: 90000
          tax_rate: 0.25
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
        tmp.write(yaml_content)
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="Invalid time_frequency: FORTNIGHT. Must be YEAR, MONTH, or DAY."):
            load_yaml_config(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_yaml_config_valid_time_frequency():
    for frequency in ["YEAR", "MONTH", "DAY"]:
        yaml_content = f"""
        start_year: 2025
        end_year: 2030
        time_frequency: "{frequency}"
        household:
          living_costs: 60000
          housing_costs: 25000
          members:
            - name: "Alice"
              income: 90000
              tax_rate: 0.25
        """
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml") as tmp:
            tmp.write(yaml_content)
            tmp_path = tmp.name

        try:
            config = load_yaml_config(tmp_path)
            assert config["time_frequency"] == frequency
        finally:
            os.remove(tmp_path)
