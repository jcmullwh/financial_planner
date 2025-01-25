# tests/test_simulation_engine.py

from decimal import ROUND_HALF_UP, Decimal

import pytest

from financial_planner.simulation_engine import SimulationEngine


@pytest.fixture
def sample_config():
    return {
        "start_year": 2024,
        "end_year": 2026,
        "inflation_rate": 0.02,
        "time_frequency": "YEAR",
        "household": {
            "living_costs": 50000.00,
            "housing_costs": 20000.00,
            "members": [
                {"name": "Jason", "income": 80000.00, "tax_rate": 0.25},
                {"name": "Linda", "income": 60000.00, "tax_rate": 0.20},
            ],
        },
    }


def test_load_scenario_valid(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    assert engine.start_year == 2024
    assert engine.end_year == 2026
    assert engine.inflation_rate == Decimal("0.0200")
    assert engine.household.living_costs == Decimal("50000.00")
    assert engine.household.housing_costs == Decimal("20000.00")
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
    assert year1["year"] == Decimal("2024")
    assert year1["total_income"] == Decimal("140000.00")  # 80000 + 60000
    assert year1["total_taxes"] == Decimal("32000.00")  # 80000*0.25 + 60000*0.20
    assert year1["total_mandatory_expenses"] == Decimal("70000.00")  # 50000 + 20000
    assert year1["leftover"] == Decimal("38000.00")  # 140000 - 32000 - 70000
    assert year1["naive_discretionary"] == Decimal("38000.00")

    # Check expenses before inflation for next year
    assert year1["living_costs"] == Decimal("50000.00")  # Initial living costs before inflation
    assert year1["housing_costs"] == Decimal("20000.00")  # Initial housing costs before inflation

    # Year 2025
    year2 = engine.results[1]
    assert year2["year"] == Decimal("2025")
    # Income updated by 3%: Jason: 80000 * 1.03 = 82400, Linda: 60000 * 1.03 = 61800
    assert year2["total_income"] == Decimal("82400.00") + Decimal("61800.00") == Decimal("144200.00")
    # Taxes: Jason: 82400 * 0.25 = 20600, Linda: 61800 * 0.20 = 12360
    assert year2["total_taxes"] == Decimal("20600.00") + Decimal("12360.00") == Decimal("32960.00")
    # Mandatory expenses: 50000 + 20000 = 70000 (before inflation for Year1)
    # Apply inflation: living_costs: 50000 * 1.02 = 51000, housing_costs: 20000 * 1.02 = 20400
    expected_mandatory = Decimal("51000.00") + Decimal("20400.00")  # 71400
    assert year2["total_mandatory_expenses"] == expected_mandatory
    # Leftover: 144200 - 32960 - 71400 = 39840
    assert year2["leftover"] == Decimal("39840.00")
    assert year2["naive_discretionary"] == Decimal("39840.00")

    # Check expenses before inflation for next year
    assert year2["living_costs"] == Decimal("51000.00")  # 50000 * 1.02
    assert year2["housing_costs"] == Decimal("20400.00")  # 20000 * 1.02

    # Year 2026
    year3 = engine.results[2]
    assert year3["year"] == Decimal("2026")
    # Income updated by 3%: Jason: 82400 * 1.03 = 84872, Linda: 61800 * 1.03 = 63654
    assert year3["total_income"] == Decimal("84872.00") + Decimal("63654.00") == Decimal("148526.00")
    # Taxes: Jason: 84872 * 0.25 = 21218, Linda: 63654 * 0.20 = 12730.8
    assert year3["total_taxes"] == Decimal("21218.00") + Decimal("12730.80") == Decimal("33948.80")
    # Expenses: 51000 + 20400 = 71400 (before inflation for Year2)
    # Apply inflation: living_costs: 51000 * 1.02 = 52020, housing_costs: 20400 * 1.02 = 20808
    expected_mandatory = Decimal("52020.00") + Decimal("20808.00")  # 72828
    assert year3["total_mandatory_expenses"] == expected_mandatory
    # Leftover: 148526 - 33948.80 - 72828 = 41249.20
    assert year3["leftover"] == Decimal("41749.20")
    assert year3["naive_discretionary"] == Decimal("41749.20")


def test_apply_house_purchase_event(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define a house_purchase event
    event = {"year": 2025, "type": "house_purchase", "principal": 300000, "interest_rate": 0.04}

    engine.apply_event(event)

    # Check that the mortgage was added
    assert len(engine.household.mortgages) == 1
    mortgage = engine.household.mortgages[0]
    assert mortgage.principal == Decimal("300000")
    assert mortgage.interest_rate == Decimal("0.04")

    # Check that housing_costs increased by mortgage's annual_payment
    expected_housing_costs = Decimal("20000.00") + mortgage.annual_payment
    assert engine.household.housing_costs == expected_housing_costs


def test_apply_new_child_event(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define a new_child event
    event = {"year": 2026, "type": "new_child"}

    initial_living_costs = engine.household.living_costs
    engine.apply_event(event)

    # Assuming each new child increases living costs by 5000
    expected_living_costs = initial_living_costs + Decimal("5000.00")
    assert engine.household.living_costs == expected_living_costs


def test_apply_job_change_event(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define a job_change event
    event = {"year": 2027, "type": "job_change", "member_name": "Jason", "new_income": 85000}

    # Find Jason's initial income
    member = engine.household.get_member_by_name("Jason")

    engine.apply_event(event)

    # Check that Jason's income is updated
    assert member.income == Decimal("85000.00")

    # Ensure that income was updated and affects aggregate_income
    total_income = engine.household.aggregate_income()
    expected_income = Decimal("85000.00") + Decimal("60000.00")
    assert total_income == expected_income


def test_apply_windfall_event(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define a windfall event
    event = {"year": 2028, "type": "windfall", "amount": 50000}

    initial_cash_reserves = engine.household.cash_reserves
    engine.apply_event(event)

    # Check that cash_reserves increased
    assert engine.household.cash_reserves == initial_cash_reserves + Decimal("50000.00")

    # Check that aggregate_income includes windfall and resets cash_reserves
    total_income = engine.household.aggregate_income()
    expected_income = Decimal("60000.00") + Decimal("80000.00") + Decimal("50000.00")
    assert total_income == expected_income
    assert engine.household.cash_reserves == Decimal("0.00")


def test_apply_multiple_events_same_year(sample_config):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define multiple events in the same year
    events = [
        {"year": 2026, "type": "house_purchase", "principal": 250000, "interest_rate": 0.035},
        {"year": 2026, "type": "new_child"},
        {"year": 2026, "type": "windfall", "amount": 20000},
    ]

    for event in events:
        engine.apply_event(event)

    # Check that all events were applied
    assert len(engine.household.mortgages) == 1
    mortgage = engine.household.mortgages[0]
    assert mortgage.principal == Decimal("250000.00")
    assert mortgage.interest_rate == Decimal("0.035")

    # Check that housing_costs include mortgage payment
    expected_housing_costs = Decimal("20000.00") + mortgage.annual_payment
    assert engine.household.housing_costs == expected_housing_costs

    # Check that living_costs increased by new_child
    expected_living_costs = Decimal("50000.00") + Decimal("5000.00")  # Assuming new_child adds 5000
    assert engine.household.living_costs == expected_living_costs

    # Check that cash_reserves increased by windfall
    assert engine.household.cash_reserves == Decimal("20000.00")


def test_apply_job_change_event_non_existent_member(sample_config, capsys):
    engine = SimulationEngine()
    engine.load_scenario(sample_config)

    # Define a job_change event for a non-existent member
    event = {
        "year": 2027,
        "type": "job_change",
        "member_name": "Charlie",  # Charlie does not exist
        "new_income": 75000,
    }

    engine.apply_event(event)

    # Capture the output to verify the warning
    captured = capsys.readouterr()
    assert "WARNING" in captured.out
    assert "Member 'Charlie' not found in household." in captured.out

    # Ensure no income was updated
    member = engine.household.get_member_by_name("Jason")
    assert member.income == Decimal("80000.00")  # Original income remains unchanged


def test_simulation_with_events():
    engine = SimulationEngine()
    config = {
        "start_year": 2025,
        "end_year": 2028,
        "inflation_rate": 0.02,
        "time_frequency": "YEAR",
        "household": {
            "living_costs": 50000.00,
            "housing_costs": 20000.00,
            "members": [
                {"name": "Jason", "income": 80000.00, "tax_rate": 0.25},
                {"name": "Linda", "income": 60000.00, "tax_rate": 0.20},
            ],
        },
        "events": [
            {"year": 2025, "type": "house_purchase", "principal": 300000, "interest_rate": 0.04},
            {"year": 2026, "type": "new_child"},
            {"year": 2027, "type": "job_change", "member_name": "Jason", "new_income": 85000},
            {"year": 2027, "type": "windfall", "amount": 50000},
        ],
    }

    engine.load_scenario(config)
    engine.run_simulation()

    assert len(engine.results) == 4  # 2025, 2026, 2027, 2028

    # Year 2025
    year1 = engine.results[0]
    assert year1["year"] == Decimal("2025")
    assert year1["total_income"] == Decimal("140000.00")  # 80000 + 60000
    assert year1["total_taxes"] == Decimal("32000.00")  # 80000*0.25 + 60000*0.20

    expected_mandatory = Decimal("50000.00") + Decimal("20000.00")
    assert year1["total_mandatory_expenses"] == expected_mandatory
    # Leftover: total_income - total_taxes - mandatory = 140000 - 32000 - 70000 = 41240
    assert year1["leftover"] == Decimal("38000.00")
    assert year1["naive_discretionary"] == Decimal("38000.00")

    # Check expenses before inflation for next year
    assert year1["living_costs"] == Decimal("50000.00")  # Initial living costs before inflation
    assert year1["housing_costs"] == Decimal("20000.00")  # Initial housing costs before inflation

    # Year 2026
    year2 = engine.results[1]
    assert year2["year"] == Decimal("2026")
    # Incomes updated by 3%: Jason: 80000 * 1.03 = 82400, Linda: 60000 * 1.03 = 61800
    assert year2["total_income"] == Decimal("82400.00") + Decimal("61800.00")
    # Taxes: Jason: 82400 * 0.25 = 20600, Linda: 61800 * 0.20 = 12360
    assert year2["total_taxes"] == Decimal("20600.00") + Decimal("12360.00") == Decimal("32960.00")
    # Check expenses before inflation for next year
    assert year2["living_costs"] == Decimal("51000.00")  # 51000
    assert year2["housing_costs"] == Decimal("20400.00") + Decimal("17349.03")  # 37749.03

    # Mandatory expenses: living_costs increased by inflation (2%), housing_costs include mortgage
    # Mortgage annual payment for 300,000 at 4% for 30 years: ~17349.03
    expected_mandatory = (
        Decimal("51000.00") + Decimal("20400.00") + Decimal("17349.03")
    )  # 51000 + 20400 + 17349.03 = 88749.03
    assert year2["total_mandatory_expenses"] == expected_mandatory
    # Leftover: 82400 + 61800 - 20600 - 12360 - 88749.03 = 144200 - 121,709.03 = 22490.97
    assert year2["leftover"] == Decimal("22490.97")
    assert year2["naive_discretionary"] == Decimal("22490.97")

    # Year 2027
    year3 = engine.results[2]
    assert year3["year"] == Decimal("2027")
    # The 2026 new_child event adds +5000 on top of the inflated living costs
    # So: living_costs = (51000 * 1.02) + 5000 = 52020 + 5000 = 57020
    # Housing costs = 20400 * 1.02 = 20808 + mortgage.annual_payment = 17696.01 = 38504.01
    # Note currently inflation is applied to mortgage payment
    # total_mandatory_expenses = 57020 + 38504.01 = 95177.03
    expected_mandatory = Decimal("57020.00") + Decimal("38504.01")
    assert year3["total_mandatory_expenses"] == expected_mandatory

    # Incomes updated by 3% over 2026 values: Jason 82400 -> 84872, Linda 61800 -> 63654
    assert year3["total_income"] == Decimal("84872.00") + Decimal("63654.00")
    expected_taxes = Decimal("84872.00") * Decimal("0.25") + Decimal("63654.00") * Decimal("0.20")
    assert year3["total_taxes"] == expected_taxes

    # leftover = total_income - total_taxes - total_mandatory_expenses
    expected_leftover = (year3["total_income"] - year3["total_taxes"] - expected_mandatory).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    assert year3["leftover"] == expected_leftover
    assert year3["naive_discretionary"] == expected_leftover

    # Year 2028
    year4 = engine.results[3]
    assert year4["year"] == Decimal("2028")
    # The 2027 "job_change" and "windfall" events are now applied
    # Check updated incomes, e.g., Jason's new_income and the added 50000 windfall
    assert year4["total_income"] == (Decimal("85000.00") + Decimal("63654.00") * Decimal("1.03") + Decimal("50000.00"))
    # ...existing checks for taxes, living_costs, housing_costs, leftover...

    # Verify that the mortgage was added in 2025
    assert len(engine.household.mortgages) == 1
    mortgage = engine.household.mortgages[0]
    assert mortgage.principal == Decimal("300000.00")
    assert mortgage.interest_rate == Decimal("0.04")
    # Check that housing_costs include mortgage payment (inflated 1 year)
    inflation_rate = Decimal(str(config["inflation_rate"]))
    expected_housing_costs = (
        Decimal("20000.00") * (Decimal("1") + inflation_rate) ** 3
        + mortgage.annual_payment * (Decimal("1") + inflation_rate) ** 2
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert engine.household.housing_costs == expected_housing_costs
