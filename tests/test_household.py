# tests/test_household.py

import pytest
from decimal import Decimal
from financial_planner.person import Person
from financial_planner.household import Household

@pytest.fixture
def household():
    member1 = Person(name="User1", income=60000.00, tax_rate=0.25, savings=6000.00)
    member2 = Person(name="User2", income=40000.00, tax_rate=0.15, savings=4000.00)
    return Household(
        members=[member1, member2],
        living_costs=50000.00,
        housing_costs=20000.00
    )

def test_household_initialization(household):
    assert len(household.members) == 2
    assert household.living_costs == Decimal('50000.00')
    assert household.housing_costs == Decimal('20000.00')

def test_aggregate_income(household):
    total_income = household.aggregate_income()
    expected_income = Decimal('60000.00') + Decimal('40000.00')
    assert total_income == expected_income

def test_aggregate_taxes(household, monkeypatch):
    # Mock calculate_taxes to return predefined values
    def mock_calculate_taxes_user1():
        return Decimal('15000.00')  # 60000 * 0.25

    def mock_calculate_taxes_user2():
        return Decimal('6000.00')   # 40000 * 0.15

    monkeypatch.setattr(household.members[0], "calculate_taxes", mock_calculate_taxes_user1)
    monkeypatch.setattr(household.members[1], "calculate_taxes", mock_calculate_taxes_user2)

    total_taxes = household.aggregate_taxes()
    expected_taxes = Decimal('15000.00') + Decimal('6000.00')
    assert total_taxes == expected_taxes

def test_total_mandatory_expenses(household):
    total_expenses = household.total_mandatory_expenses()
    expected_expenses = Decimal('50000.00') + Decimal('20000.00')
    assert total_expenses == expected_expenses

def test_apply_inflation(household):
    inflation_rate = 0.02  # 2%
    household.apply_inflation(inflation_rate)
    expected_living = (Decimal('50000.00') * Decimal('1.02')).quantize(Decimal('0.01'))
    expected_housing = (Decimal('20000.00') * Decimal('1.02')).quantize(Decimal('0.01'))
    assert household.living_costs == expected_living
    assert household.housing_costs == expected_housing

def test_household_no_members():
    household = Household(members=[], living_costs=30000.00, housing_costs=15000.00)
    assert household.aggregate_income() == Decimal('0.00')
    assert household.aggregate_taxes() == Decimal('0.00')
    assert household.total_mandatory_expenses() == Decimal('45000.00')

def test_household_zero_expenses():
    member = Person(name="User", income=50000.00, tax_rate=0.20)
    household = Household(members=[member], living_costs=0.00, housing_costs=0.00)
    assert household.total_mandatory_expenses() == Decimal('0.00')

def test_household_negative_expenses():
    member = Person(name="User", income=50000.00, tax_rate=0.20)
    household = Household(members=[member], living_costs=-1000.00, housing_costs=-500.00)
    expected_expenses = Decimal('-1000.00') + Decimal('-500.00')
    assert household.total_mandatory_expenses() == expected_expenses
