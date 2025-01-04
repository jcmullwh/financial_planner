# tests/test_simulation_engine.py

import pytest
from decimal import Decimal
from financial_planner.simulation_engine import SimulationEngine
from financial_planner.person import Person
from financial_planner.household import Household

@pytest.fixture
def sample_config():
    return {
        "start_year": 2024,
        "end_year": 2026,
        "inflation_rate": 0.02,
        "household": {
            "living_costs": 50000.00,
            "housing_costs": 20000.00,
            "members": [
                {"name": "Jason", "income": 80000.00, "tax_rate": 0.25},
                {"name": "Linda", "income": 60000.00, "tax_rate": 0.20}
            ]
        }
    }

def test_load_scenario_valid(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)
    
    assert engine.start_year == 2024
    assert engine.end_year == 2026
    assert engine.inflation_rate == Decimal('0.0200')
    assert engine.household.living_costs == Decimal('50000.00')
    assert engine.household.housing_costs == Decimal('20000.00')
    assert len(engine.household.members) == 2
    assert engine.household.members[0].name == "Jason"
    assert engine.household.members[1].name == "Linda"

def test_load_scenario_missing_field(sample_config):
    engine = SimulationEngine()
    incomplete_config = sample_config.copy()
    del incomplete_config["start_year"]
    with pytest.raises(ValueError, match="Missing required configuration field: 'start_year'"):
        engine.load_scenario(incomplete_config)

def test_load_scenario_invalid_value(sample_config):
    engine = SimulationEngine()
    invalid_config = sample_config.copy()
    invalid_config["end_year"] = "two thousand and twenty-six"  # Non-convertible string
    with pytest.raises(ValueError, match="Invalid configuration value"):
        engine.load_scenario(invalid_config)

def test_run_simulation(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)
    engine.run_simulation()
    
    assert len(engine.results) == 3  # 2024, 2025, 2026
    
    # Year 2024
    year1 = engine.results[0]
    assert year1["year"] == Decimal('2024')
    assert year1["total_income"] == Decimal('144200.00')  # 82400 + 61800
    assert year1["total_taxes"] == Decimal('32960.00')    # 82400*0.25 + 61800*0.20
    assert year1["total_mandatory_expenses"] == Decimal('70000.00')  # 50000 + 20000
    assert year1["leftover"] == Decimal('41240.00')     # 144200 - 32960 - 70000
    assert year1["naive_discretionary"] == Decimal('41240.00')
    
    # Check expenses before inflation for next year
    assert year1["living_costs"] == Decimal('50000.00')  # Initial living costs before inflation
    assert year1["housing_costs"] == Decimal('20000.00')  # Initial housing costs before inflation
    
    # Year 2025
    year2 = engine.results[1]
    assert year2["year"] == Decimal('2025')
    # Income updated by 3%: Jason: 82400 * 1.03 = 84872, Linda: 61800 * 1.03 = 63654
    assert year2["total_income"] == Decimal('84872.00') + Decimal('63654.00') == Decimal('148526.00')
    # Taxes: Jason: 84872 * 0.25 = 21218, Linda: 63654 * 0.20 = 12730.8
    assert year2["total_taxes"] == Decimal('21218.00') + Decimal('12730.80') == Decimal('33948.80')
    # Expenses: 50000 + 20000 = 70000 (before inflation for Year1)
    assert year2["total_mandatory_expenses"] == Decimal('71400.00')  # 70000 * 1.02
    # Leftover: 148526 - 33948.80 - 71400 = 43177.20
    assert year2["leftover"] == Decimal('43177.20')
    assert year2["naive_discretionary"] == Decimal('43177.20')
    
    # Check expenses before inflation for next year
    assert year2["living_costs"] == Decimal('51000.00')  # 50000 * 1.02
    assert year2["housing_costs"] == Decimal('20400.00')  # 20000 * 1.02
    
    # Year 2026
    year3 = engine.results[2]
    assert year3["year"] == Decimal('2026')
    # Income updated by 3%: Jason: 84872 * 1.03 = 87418.16, Linda: 63654 * 1.03 = 65563.62
    assert year3["total_income"] == Decimal('87418.16') + Decimal('65563.62') == Decimal('152981.78')
    # Taxes: Jason: 87418.16 * 0.25 = 21854.54, Linda: 65563.62 * 0.20 = 13112.72
    assert year3["total_taxes"] == Decimal('21854.54') + Decimal('13112.72') == Decimal('34967.26')
    # Expenses: 51000 + 20400 = 71400 (before inflation for Year2)
    assert year3["total_mandatory_expenses"] == Decimal('72828.00')  # 71400 * 1.02
    # Leftover: 152,981.78 - 34,967.26 - 72,828.00 = 45,186.52
    assert year3["leftover"] == Decimal('45186.52')
    assert year3["naive_discretionary"] == Decimal('45186.52')
    
    # Check expenses before inflation for next year (no further years, so no inflation applied)
    assert year3["living_costs"] == Decimal('52020.00')  # 51000 * 1.02
    assert year3["housing_costs"] == Decimal('20808.00')  # 20400 * 1.02

def test_run_simulation_no_inflation(sample_config):
    config_no_inflation = sample_config.copy()
    config_no_inflation["inflation_rate"] = 0.00
    engine = SimulationEngine()
    engine.load_scenario(config_no_inflation)
    engine.run_simulation()
    
    assert len(engine.results) == 3
    
    # Expenses should remain constant
    for year_result in engine.results:
        assert year_result["total_mandatory_expenses"] == Decimal('70000.00')
    
    # No inflation applied
    household = engine.household
    assert household.living_costs == Decimal('50000.00')
    assert household.housing_costs == Decimal('20000.00')

def test_run_simulation_not_initialized():
    engine = SimulationEngine()
    with pytest.raises(RuntimeError, match="SimulationEngine is not properly initialized"):
        engine.run_simulation()
