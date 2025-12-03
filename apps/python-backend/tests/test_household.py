# tests/test_household.py
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from financial_planner.household import Household
from financial_planner.person import Person
from financial_planner.contracts import MortgageContract, EmploymentContract, RentContract
from financial_planner.state import Liability
from financial_planner.transactions import Transaction

# A fixture that builds a Household with two Persons.
@pytest.fixture
def household():
    hh = Household()
    p1 = Person("User1")
    p2 = Person("User2")
    hh.add_member(p1)
    hh.add_member(p2)
    return hh

def test_household_initialization(household):
    # Check that household has 2 members and an empty timeline.
    assert len(household.members) == 2
    assert household.timeline.get_transactions() == []

def test_aggregate_income(household):
    # Manually add some positive transactions to the household timeline.
    t1 = Transaction(timestamp=datetime(2025, 1, 1), amount=5000.00, category="salary")
    t2 = Transaction(timestamp=datetime(2025, 1, 15), amount=3000.00, category="salary")
    household.timeline.add_transaction(t1)
    household.timeline.add_transaction(t2)
    
    agg_txs = household.aggregate_transactions(datetime(2025, 1, 1), datetime(2025, 1, 31))
    total_income = sum(Decimal(str(tx.amount)) for tx in agg_txs if tx.amount > 0)
    expected_income = Decimal("5000.00") + Decimal("3000.00")
    assert total_income == expected_income

def test_add_windfall(household):
    # Simulate a windfall by adding a one-off transaction to the household timeline.
    windfall_amount = Decimal("10000.00")
    t = Transaction(timestamp=datetime(2025, 2, 1), amount=float(windfall_amount), category="windfall")
    household.timeline.add_transaction(t)
    
    agg_txs = household.aggregate_transactions(datetime(2025, 2, 1), datetime(2025, 2, 1))
    total_income = sum(Decimal(str(tx.amount)) for tx in agg_txs if tx.amount > 0)
    assert total_income == windfall_amount

def test_add_mortgage(household):
    # Create a mortgage contract and add it to the household.
    principal = Decimal("300000.00")
    interest_rate = Decimal("0.04")
    term_years = 30
    # Create a liability object that the contract will update.
    liability = Liability("Mortgage", principal)
    mortgage_contract = MortgageContract(
        start_date=datetime(2025, 3, 1),
        principal=principal,
        annual_interest_rate=interest_rate,
        term_years=term_years,
        liability=liability
    )
    
    initial_contract_count = len(household.contracts)
    household.add_contract(mortgage_contract)
    assert len(household.contracts) == initial_contract_count + 1

    # Generate mortgage transactions over a few months.
    household.timeline.generate_transactions(datetime(2025, 6, 1))
    txs = household.timeline.get_transactions()
    mortgage_txs = [tx for tx in txs if tx.category in ("mortgage_interest", "mortgage_principal")]
    assert len(mortgage_txs) > 0

def test_employment_contract(household):
    # Attach an employment contract to one Person.
    person = household.members[0]
    salary = Decimal("4000.00")
    contract = EmploymentContract(
        start_date=datetime(2025, 1, 1),
        salary=salary,
        interval=timedelta(days=30),
        person_name=person.name
    )
    initial_contract_count = len(person.contracts)
    person.add_contract(contract)
    assert len(person.contracts) == initial_contract_count + 1

    # Generate salary transactions over two months.
    person.timeline.generate_transactions(datetime(2025, 3, 1))
    txs = person.timeline.get_transactions()
    salary_txs = [tx for tx in txs if tx.category == "salary" and tx.metadata.get("person") == person.name]
    # Expect at least two salary transactions.
    assert len(salary_txs) >= 2

def test_rent_contract(household):
    # Add a rent contract to the household.
    monthly_rent = Decimal("1200.00")
    contract = RentContract(
        start_date=datetime(2025, 4, 1),
        monthly_rent=monthly_rent
    )
    initial_contract_count = len(household.contracts)
    household.add_contract(contract)
    assert len(household.contracts) == initial_contract_count + 1

    # Generate rent transactions for three months.
    household.timeline.generate_transactions(datetime(2025, 7, 1))
    txs = household.timeline.get_transactions()
    rent_txs = [tx for tx in txs if tx.category == "rent"]
    assert len(rent_txs) >= 3

def test_compute_net_worth(household):
    # Add assets and liabilities at both the household and person levels.
    from financial_planner.state import Asset, Liability
    # Household-level asset and liability.
    asset_house = Asset("House", Decimal("350000.00"), datetime(2025, 1, 1))
    liability_mortgage = Liability("Mortgage", Decimal("300000.00"))
    household.add_asset(asset_house)
    household.add_liability(liability_mortgage)
    
    # Person-level asset and liability.
    person = household.members[0]
    asset_car = Asset("Car", Decimal("20000.00"), datetime(2025, 2, 1))
    liability_car_loan = Liability("Car Loan", Decimal("15000.00"))
    person.add_asset(asset_car)
    person.add_liability(liability_car_loan)
    
    net_worth = household.compute_net_worth()
    expected_net = Decimal("350000.00") - Decimal("300000.00") + Decimal("20000.00") - Decimal("15000.00")
    assert net_worth == expected_net

# The following tests from the previous phase were removed:
# - Tests referencing 'living_costs', 'housing_costs', 'cash_reserves', aggregate_taxes,
#   Mortgage.make_payment, and Mortgage.is_active are no longer relevant in the new design.
