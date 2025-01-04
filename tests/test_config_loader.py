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
        config = load_yaml_config(tmp_path)
        assert config is None
    finally:
        os.remove(tmp_path)
