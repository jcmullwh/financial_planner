# tests/test_household.py

from decimal import Decimal

import pytest

from financial_planner.household import Household, Mortgage
from financial_planner.person import Person


@pytest.fixture
def household():
    member1 = Person(name="User1", income=60000.00, tax_rate=0.25, savings=6000.00)
    member2 = Person(name="User2", income=40000.00, tax_rate=0.15, savings=4000.00)
    return Household(members=[member1, member2], living_costs=50000.00, housing_costs=20000.00)


def test_household_initialization(household):
    assert len(household.members) == 2
    assert household.living_costs == Decimal("50000.00")
    assert household.housing_costs == Decimal("20000.00")


def test_aggregate_income(household):
    total_income = household.aggregate_income()
    expected_income = Decimal("60000.00") + Decimal("40000.00")
    assert total_income == expected_income


def test_aggregate_taxes(household, monkeypatch):
    # Mock calculate_taxes to return predefined values
    def mock_calculate_taxes_user1():
        return Decimal("15000.00")  # 60000 * 0.25

    def mock_calculate_taxes_user2():
        return Decimal("6000.00")  # 40000 * 0.15

    monkeypatch.setattr(household.members[0], "calculate_taxes", mock_calculate_taxes_user1)
    monkeypatch.setattr(household.members[1], "calculate_taxes", mock_calculate_taxes_user2)

    total_taxes = household.aggregate_taxes()
    expected_taxes = Decimal("15000.00") + Decimal("6000.00")
    assert total_taxes == expected_taxes


def test_total_mandatory_expenses(household):
    total_expenses = household.total_mandatory_expenses()
    expected_expenses = Decimal("50000.00") + Decimal("20000.00")
    assert total_expenses == expected_expenses


def test_apply_inflation(household):
    inflation_rate = 0.02  # 2%
    household.apply_inflation(inflation_rate)
    expected_living = (Decimal("50000.00") * Decimal("1.02")).quantize(Decimal("0.01"))
    expected_housing = (Decimal("20000.00") * Decimal("1.02")).quantize(Decimal("0.01"))
    assert household.living_costs == expected_living
    assert household.housing_costs == expected_housing


def test_household_no_members():
    household = Household(members=[], living_costs=30000.00, housing_costs=15000.00)
    assert household.aggregate_income() == Decimal("0.00")
    assert household.aggregate_taxes() == Decimal("0.00")
    assert household.total_mandatory_expenses() == Decimal("45000.00")


def test_household_zero_expenses():
    member = Person(name="User", income=50000.00, tax_rate=0.20)
    household = Household(members=[member], living_costs=0.00, housing_costs=0.00)
    assert household.total_mandatory_expenses() == Decimal("0.00")


def test_household_negative_expenses():
    member = Person(name="User", income=50000.00, tax_rate=0.20)
    household = Household(members=[member], living_costs=-1000.00, housing_costs=-500.00)
    expected_expenses = Decimal("-1000.00") + Decimal("-500.00")
    assert household.total_mandatory_expenses() == expected_expenses


# New Tests for Phase 2


def test_add_mortgage(household):
    principal = Decimal("300000.00")
    interest_rate = Decimal("0.04")
    mortgage = Mortgage(principal=principal, interest_rate=interest_rate, term_years=30)

    initial_housing_costs = household.housing_costs
    household.add_mortgage(mortgage)

    assert len(household.mortgages) == 1
    assert household.mortgages[0].principal == principal
    assert household.mortgages[0].interest_rate == interest_rate
    assert household.housing_costs == initial_housing_costs + mortgage.annual_payment


def test_increase_living_costs(household):
    additional_expense = Decimal("7000.00")
    initial_living_costs = household.living_costs
    household.increase_living_costs(additional_expense)
    assert household.living_costs == initial_living_costs + additional_expense


def test_add_windfall(household):
    windfall_amount = Decimal("50000.00")
    initial_cash_reserves = household.cash_reserves
    household.add_windfall(windfall_amount)
    assert household.cash_reserves == initial_cash_reserves + windfall_amount

    # Test aggregate_income includes windfall and resets cash_reserves
    total_income = household.aggregate_income()
    expected_income = Decimal("60000.00") + Decimal("40000.00") + windfall_amount
    assert total_income == expected_income
    assert household.cash_reserves == Decimal("0.00")


def test_add_multiple_mortgages(household):
    mortgage1 = Mortgage(principal=Decimal("200000.00"), interest_rate=Decimal("0.035"), term_years=15)
    mortgage2 = Mortgage(principal=Decimal("150000.00"), interest_rate=Decimal("0.04"), term_years=20)

    initial_housing_costs = household.housing_costs
    household.add_mortgage(mortgage1)
    household.add_mortgage(mortgage2)

    assert len(household.mortgages) == 2
    assert household.housing_costs == initial_housing_costs + mortgage1.annual_payment + mortgage2.annual_payment


def test_aggregate_income_with_windfall(household):
    windfall_amount = Decimal("10000.00")
    household.add_windfall(windfall_amount)

    total_income = household.aggregate_income()
    expected_income = Decimal("60000.00") + Decimal("40000.00") + windfall_amount
    assert total_income == expected_income
    assert household.cash_reserves == Decimal("0.00")


def test_mortgage_calculation():
    principal = Decimal("300000.00")
    interest_rate = Decimal("0.04")
    term_years = 30
    mortgage = Mortgage(principal=principal, interest_rate=interest_rate, term_years=term_years)

    # Expected annual payment calculation
    # Using formula: P * (r * (1 + r)^n) / ((1 + r)^n - 1)
    # For 300,000 at 4% over 30 years:
    # payment ≈ 17991.60
    expected_payment = Decimal("17349.03")
    assert mortgage.annual_payment == expected_payment


def test_mortgage_make_payment():
    principal = Decimal("100000.00")
    interest_rate = Decimal("0.05")
    term_years = 10
    mortgage = Mortgage(principal=principal, interest_rate=interest_rate, term_years=term_years)

    initial_balance = mortgage.remaining_balance
    payment = mortgage.make_payment()

    expected_interest_payment = (initial_balance * interest_rate).quantize(Decimal("0.01"))
    expected_principal_payment = mortgage.annual_payment - expected_interest_payment
    assert payment == expected_principal_payment
    assert mortgage.remaining_balance == initial_balance - expected_principal_payment


def test_mortgage_is_active():
    principal = Decimal("50000.00")
    interest_rate = Decimal("0.05")
    term_years = 1
    mortgage = Mortgage(principal=principal, interest_rate=interest_rate, term_years=term_years)

    assert mortgage.is_active() == True
    mortgage.make_payment()  # This should pay off the mortgage
    assert mortgage.is_active() == False
