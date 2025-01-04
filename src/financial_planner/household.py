# financial_planner/household.py

from decimal import ROUND_HALF_UP, Decimal
from typing import List

from .person import Person


class Household:
    """
    Aggregates multiple Person objects and manages shared financial obligations
    such as living and housing costs.
    """

    def __init__(self, members: List[Person], living_costs: float, housing_costs: float):
        """
        Initializes a Household instance.

        Args:
            members (List[Person]): A list of Person objects representing the household members.
            living_costs (float): Annual mandatory living expenses (e.g., groceries, utilities).
            housing_costs (float): Annual housing-related expenses (e.g., rent, mortgage).
        """
        self.members = members
        self.living_costs = Decimal(living_costs).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.housing_costs = Decimal(housing_costs).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def aggregate_income(self) -> Decimal:
        """
        Sums the incomes of all household members.

        Returns:
            Decimal: The total household income for the current year.
        """
        total_income = sum(member.income for member in self.members)
        print(f"[DEBUG] Aggregated household income: {total_income}.")
        return total_income

    def aggregate_taxes(self) -> Decimal:
        """
        Sums the taxes owed by all household members.

        Returns:
            Decimal: The total taxes for the household for the current year.
        """
        total_taxes = sum(member.calculate_taxes() for member in self.members)
        print(f"[DEBUG] Aggregated household taxes: {total_taxes}.")
        return total_taxes

    def total_mandatory_expenses(self) -> Decimal:
        """
        Calculates the sum of all mandatory expenses, including living and housing costs.

        Returns:
            Decimal: The total mandatory expenses for the household for the current year.
        """
        total_expenses = self.living_costs + self.housing_costs
        print(f"[DEBUG] Total mandatory expenses: {total_expenses}.")
        return total_expenses

    def apply_inflation(self, inflation_rate: float) -> None:
        """
        Applies the annual inflation rate to living and housing costs.

        Args:
            inflation_rate (float): The annual inflation rate as a decimal (e.g., 0.02 for 2%).
        """
        rate = Decimal(inflation_rate).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        self.living_costs = (self.living_costs * (Decimal("1") + rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        self.housing_costs = (self.housing_costs * (Decimal("1") + rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        print(f"[DEBUG] Applied inflation rate of {inflation_rate*100}% to living and housing costs.")
