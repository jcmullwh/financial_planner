# financial_planner/__init__.py

from importlib.metadata import version

try:
    __version__ = version("financial_planner")
except Exception:  # pragma: no cover - fallback for missing package metadata
    __version__ = "0.0.0"

from .config_loader import load_yaml_config
from .household import Household
from .person import Person
from .report_generator import generate_report
from .simulation_engine import SimulationEngine

__all__ = ["Household", "Person", "SimulationEngine", "generate_report", "load_yaml_config"]
