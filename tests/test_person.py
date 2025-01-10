# tests/test_person.py

from decimal import Decimal

import pytest

from financial_planner.person import Person


@pytest.fixture
def person():
    return Person(name="Test User", income=50000.00, tax_rate=0.20, savings=5000.00)


def test_person_initialization(person):
    assert person.name == "Test User"
    assert person.income == Decimal("50000.00")
    assert person.tax_rate == Decimal("0.2000")
    assert person.savings == Decimal("5000.00")


def test_update_income(person):
    original_income = person.income
    person.update_income(year=2025)
    expected_income = (original_income * Decimal("1.03")).quantize(Decimal("0.01"))
    assert person.income == expected_income


def test_update_income_multiple_years(person):
    # Update income for 3 consecutive years
    for year in range(2025, 2028):
        person.update_income(year)
    expected_income = Decimal("50000.00") * Decimal("1.03") ** 3
    expected_income = expected_income.quantize(Decimal("0.01"))
    assert person.income == expected_income


def test_calculate_taxes(person):
    expected_taxes = (person.income * Decimal("0.20")).quantize(Decimal("0.01"))
    assert person.calculate_taxes() == expected_taxes


def test_calculate_taxes_zero_tax(person):
    person.tax_rate = Decimal("0.00")
    assert person.calculate_taxes() == Decimal("0.00")


def test_calculate_taxes_zero_income(person):
    person.income = Decimal("0.00")
    expected_taxes = Decimal("0.00")
    assert person.calculate_taxes() == expected_taxes


# New Tests for Phase 2


def test_update_income_specific(person):
    new_income = Decimal("75000.00")
    person.update_income_specific(new_income)
    assert person.income == new_income


def test_update_income_specific_negative(person):
    # Assuming the update_income_specific method should not allow negative incomes
    # Modify the Person class to raise ValueError if new_income is negative
    with pytest.raises(ValueError, match="Income cannot be negative."):
        person.update_income_specific(Decimal("-5000.00"))
