# financial_planner/person.py

from decimal import ROUND_HALF_UP, Decimal


class Person:
    """
    Represents an individual within a household, encapsulating personal financial details
    such as income and tax obligations.
    """

    def __init__(self, name: str, income: float, tax_rate: float, savings: float = 0.0):
        """
        Initializes a Person instance.

        Args:
            name (str): The identifier for the person (e.g., "Jason").
            income (float): The annual income of the person.
            tax_rate (float): The flat tax rate applicable to the person's income (e.g., 0.25 for 25%).
            savings (float, optional): The amount allocated to savings each year. Defaults to 0.0.
        """
        self.name = name
        self.income = Decimal(income).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.tax_rate = Decimal(tax_rate).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        self.savings = Decimal(savings).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def update_income(self, year: int) -> None:
        """
        Adjusts the person's income based on the simulation year.
        This method applies a fixed annual growth rate to the income.

        Args:
            year (int): The current year in the simulation.
        """
        growth_rate = Decimal("0.03")  # 3% annual income growth
        self.income = (self.income * (Decimal("1") + growth_rate)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"[DEBUG] {self.name}'s income updated to {self.income} for year {year}.")

    def update_income_specific(self, new_income: Decimal) -> None:
        """
        Sets the person's income to a specific value, used for job changes.

        Args:
            new_income (Decimal): The new income value to set.

        Raises:
            ValueError: If the new_income is negative.
        """
        if new_income < 0:
            error_message = "Income cannot be negative."
            raise ValueError(error_message)
        self.income = new_income.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"[DEBUG] {self.name}'s income explicitly set to {self.income}.")

    def calculate_taxes(self) -> Decimal:
        """
        Computes the taxes owed by the person based on their current income and tax rate.

        Returns:
            Decimal: The total tax amount for the current year.
        """
        taxes = (self.income * self.tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"[DEBUG] {self.name}'s taxes calculated as {taxes}.")
        return taxes
