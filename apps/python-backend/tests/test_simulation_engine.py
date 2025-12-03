# tests/test_simulation_engine.py
from datetime import datetime, timedelta
from decimal import Decimal
import pytest

from financial_planner.simulation_engine import SimulationEngine
from financial_planner.events import (
    MortgagePurchaseEvent,
    WindfallEvent,
    EmploymentChangeEvent,
    NewChildEvent,
)
from financial_planner.person import Person
from financial_planner.contracts import EmploymentContract

@pytest.fixture
def sim_engine_with_events():
    """
    Build a simulation engine with:
      - Start: Jan 1, 2025; End: Jan 1, 2029; yearly time steps.
      - Two employment contracts for Jason and Linda starting on 2025-01-01.
        * Jason: annual income 80,000 (monthly ≈ 80,000/12)
        * Linda: annual income 60,000 (monthly = 60,000/12)
      - MortgagePurchaseEvent at 2025-06-01 for 300,000 at 4% (30 years).
      - NewChildEvent at 2026-06-01 (–5,000).
      - EmploymentChangeEvent on 2027-01-01 for Jason to 85,000 annually.
      - WindfallEvent on 2027-06-01 for 50,000.
      
      With the current engine design, snapshots are recorded at the end of each step.
      (Thus, with start 2025-01-01 and a 1-year step, we expect snapshots at:
         index 0: 2026-01-01,
         index 1: 2027-01-01,
         index 2: 2028-01-01,
         index 3: 2029-01-01,
         index 4: 2029-01-01 (duplicate final snapshot).)
    """
    engine = SimulationEngine(
        start_time=datetime(2025, 1, 1),
        end_time=datetime(2029, 1, 1),
        time_step=timedelta(days=365)
    )
    # Add two members.
    jason = Person("Jason")
    linda = Person("Linda")
    engine.household.add_member(jason)
    engine.household.add_member(linda)

    # Add employment contracts for both starting on 2025-01-01.
    emp_jason = EmploymentContract(
        start_date=datetime(2025, 1, 1),
        salary=Decimal("80000.00") / Decimal("12"),
        interval=timedelta(days=30),
        person_name="Jason"
    )
    emp_linda = EmploymentContract(
        start_date=datetime(2025, 1, 1),
        salary=Decimal("60000.00") / Decimal("12"),
        interval=timedelta(days=30),
        person_name="Linda"
    )
    jason.add_contract(emp_jason)
    linda.add_contract(emp_linda)

    # Schedule MortgagePurchaseEvent at 2025-06-01.
    mortgage_event = MortgagePurchaseEvent(
        event_time=datetime(2025, 6, 1),
        data={
            "principal": "300000",
            "interest_rate": "0.04",
            "term_years": 30
        }
    )
    engine.add_event(mortgage_event)

    # Schedule NewChildEvent at 2026-06-01.
    child_event = NewChildEvent(
        event_time=datetime(2026, 6, 1),
        data={}
    )
    engine.add_event(child_event)

    # Schedule EmploymentChangeEvent for Jason on 2027-01-01.
    emp_change = EmploymentChangeEvent(
        event_time=datetime(2027, 1, 1),
        data={
            "person_name": "Jason",
            "new_salary": "85000",
            "interval_days": 30
        }
    )
    engine.add_event(emp_change)

    # Schedule WindfallEvent on 2027-06-01.
    windfall_event = WindfallEvent(
        event_time=datetime(2027, 6, 1),
        data={"amount": "50000"}
    )
    engine.add_event(windfall_event)

    return engine

def test_simulation_with_events(sim_engine_with_events):
    """
    Run the simulation and verify that snapshots contain correct (approximate)
    cumulative figures.
    
    We expect 5 snapshots:
      Snapshot 0: at 2026-01-01 (end of 2025)
      Snapshot 1: at 2027-01-01 (end of 2026)
      Snapshot 2: at 2028-01-01 (end of 2027)
      Snapshot 3: at 2029-01-01 (end of 2028)
      Snapshot 4: at 2029-01-01 (final snapshot; duplicate final time)
    
    Calculations (approximate):
    
    -- Snapshot 0 (2026-01-01):
       Employment income in 2025: ~13 payments per contract:
         Jason: 13×(80000/12) ≈ 151666.67,
         Linda: 13×(60000/12) = 65000.00.
         Total ≈ 151666.67.
       Mortgage from 2025-06-01 to 2026-01-01:
         Using _add_months, 8 payments × ~1431.90 ≈ 11455.20 expense.
       Expected net ≈ 151666.67 – 11455.20 = 140211.47.
    
    -- Snapshot 1 (2027-01-01):
       Additional 2026 employment: ~151666.67,
         Cumulative ≈ 151666.67 + 151666.67 = 303333.34.
       Mortgage from 2025-06-01 to 2027-01-01:
         20 payments × 1431.90 ≈ 28638.00.
       NewChildEvent: –5000.
       Total expenses ≈ 28638.00 + 5000 = 33638.00.
       Expected net ≈ 303333.34 – 33638.00 = 269695.34.
    
    -- Snapshot 2 (2028-01-01):
       In 2027, after Jason’s change:
         Jason: 13×(85000/12) ≈ 92083.33,
         Linda: 13×(60000/12) = 65000.00,
         2027 total ≈ 157083.33.
       Cumulative employment becomes ≈ 303333.34 + 157083.33 = 460416.67.
       Adding windfall of 50000 → Total ≈ 510416.67.
       Mortgage from 2025-06-01 to 2028-01-01:
         32 payments × 1431.90 ≈ 45820.80.
       Total expenses ≈ 45820.80 + 5000 = 50820.80.
       Expected net ≈ 510416.67 – 50820.80 = 459595.87.
    
    -- Snapshot 3 (2029-01-01):
       2028 employment: another ~157083.33,
         Cumulative employment becomes ≈ 510416.67 + 157083.33 = 667500.00.
       Mortgage from 2025-06-01 to 2029-01-01:
         45 payments × 1431.90 ≈ 64435.50.
       Total expenses ≈ 64435.50 + 5000 = 69435.50.
       Expected net ≈ 667500.00 – 69435.50 = 598064.50.
    
    -- Snapshot 4: Duplicate of snapshot 3.
    """
    engine = sim_engine_with_events
    engine.run()
    results = engine.results
    # Expect 5 snapshots.
    assert len(results) == 5

    # Snapshot 0: at 2026-01-01
    snap0 = results[0]
    assert snap0["time"] == datetime(2026, 1, 1)
    expected_income_2025 = Decimal("151666.67")
    expected_expenses_2025 = Decimal("11455.20")
    expected_net_2025 = expected_income_2025 - expected_expenses_2025
    assert float(snap0["income"]) == pytest.approx(float(expected_income_2025), rel=1e-2)
    assert float(snap0["expenses"]) == pytest.approx(-float(expected_expenses_2025), rel=1e-2)
    assert float(snap0["net"]) == pytest.approx(float(expected_net_2025), rel=1e-2)

    # Snapshot 1: at 2027-01-01
    snap1 = results[1]
    assert snap1["time"] == datetime(2027, 1, 1)
    expected_income_2026 = Decimal("303333.34")
    expected_mortgage_2026 = Decimal("28638.00")
    expected_expenses_2026 = expected_mortgage_2026 + Decimal("5000.00")
    expected_net_2026 = expected_income_2026 - expected_expenses_2026
    assert float(snap1["income"]) == pytest.approx(float(expected_income_2026), rel=1e-2)
    assert float(snap1["expenses"]) == pytest.approx(-float(expected_expenses_2026), rel=1e-2)
    assert float(snap1["net"]) == pytest.approx(float(expected_net_2026), rel=1e-2)

    # Snapshot 2: at 2028-01-01
    snap2 = results[2]
    assert snap2["time"] == datetime(2028, 1, 1)
    expected_income_2027 = Decimal("510416.67")  # cumulative including windfall
    expected_mortgage_2027 = Decimal("45820.80")
    expected_expenses_2027 = expected_mortgage_2027 + Decimal("5000.00")
    expected_net_2027 = expected_income_2027 - expected_expenses_2027
    assert float(snap2["income"]) == pytest.approx(float(expected_income_2027), rel=1e-2)
    assert float(snap2["expenses"]) == pytest.approx(-float(expected_expenses_2027), rel=1e-2)
    assert float(snap2["net"]) == pytest.approx(float(expected_net_2027), rel=1e-2)

    # Snapshot 3: at 2029-01-01
    snap3 = results[3]
    assert snap3["time"] == datetime(2029, 1, 1)
    expected_income_2028 = Decimal("667500.00")
    expected_mortgage_2028 = Decimal("64435.50")
    expected_expenses_2028 = expected_mortgage_2028 + Decimal("5000.00")
    expected_net_2028 = expected_income_2028 - expected_expenses_2028
    assert float(snap3["income"]) == pytest.approx(float(expected_income_2028), rel=1e-2)
    assert float(snap3["expenses"]) == pytest.approx(-float(expected_expenses_2028), rel=1e-2)
    assert float(snap3["net"]) == pytest.approx(float(expected_net_2028), rel=1e-2)

    # Snapshot 4: duplicate final snapshot.
    snap4 = results[4]
    assert snap4["time"] == datetime(2029, 1, 1)
    assert float(snap4["income"]) == pytest.approx(float(expected_income_2028), rel=1e-2)
    assert float(snap4["expenses"]) == pytest.approx(-float(expected_expenses_2028), rel=1e-2)
    assert float(snap4["net"]) == pytest.approx(float(expected_net_2028), rel=1e-2)

    # Verify that household net worth is nonnegative.
    assert float(snap4["household_net_worth"]) >= 0.0
