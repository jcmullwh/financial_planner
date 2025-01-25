# financial_planner/household.py

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from .person import Person


class Mortgage:
    """
    Represents a mortgage loan with principal, interest rate, and term details.
    """

    def __init__(self, principal: Decimal, interest_rate: Decimal, term_years: int = 30) -> None:
        """
        Initializes a Mortgage instance.

        Args:
            principal (Decimal): The initial loan amount.
            interest_rate (Decimal): The annual interest rate (e.g., 0.04 for 4%).
            term_years (int, optional): The duration of the mortgage in years. Defaults to 30.
        """
        self.principal = principal
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.remaining_balance = principal
        self.annual_payment = self.calculate_annual_payment()

    def calculate_annual_payment(self) -> Decimal:
        """
        Calculates the fixed annual payment based on the principal, interest rate, and term.

        Returns:
            Decimal: The annual mortgage payment.
        """
        rate = self.interest_rate
        n = self.term_years
        if rate == 0:
            payment = self.principal / Decimal(n)
        else:
            payment = self.principal * (rate * (1 + rate) ** n) / ((1 + rate) ** n - 1)
        return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def make_payment(self) -> Decimal:
        """
        Processes an annual mortgage payment, reducing the remaining balance.

        Returns:
            Decimal: The amount paid towards the principal.
        """
        interest_payment = (self.remaining_balance * self.interest_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        principal_payment = (self.annual_payment - interest_payment).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.remaining_balance -= principal_payment
        self.remaining_balance = self.remaining_balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        debug_message = f"[DEBUG] Mortgage payment made: Principal Paid={principal_payment}"
        debug_message += f", Remaining Balance={self.remaining_balance}"
        print(debug_message)
        return principal_payment

    def is_active(self) -> bool:
        """
        Checks if the mortgage is still active (i.e., has a remaining balance).

        Returns:
            bool: True if the mortgage is active, False otherwise.
        """
        return self.remaining_balance > 0


class Household:
    """
    Aggregates multiple Person objects and manages shared financial obligations
    such as living and housing costs.
    """

    def __init__(self, members: list[Person], living_costs: float, housing_costs: float):
        """
        Initializes a Household instance.

        Args:
            members (list[Person]): A list of Person objects representing the household members.
            living_costs (float): Annual mandatory living expenses (e.g., groceries, utilities).
            housing_costs (float): Annual housing-related expenses (e.g., rent, mortgage).
        """
        self.members = members
        self.living_costs = Decimal(living_costs).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.housing_costs = Decimal(housing_costs).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.mortgages: list[Mortgage] = []  # Replaced List with list
        self.cash_reserves: Decimal = Decimal("0.00")  # To handle windfalls

    def add_mortgage(self, mortgage: Mortgage) -> None:
        """
        Adds a mortgage to the household.

        Args:
            mortgage (Mortgage): The Mortgage instance to add.
        """
        self.mortgages.append(mortgage)
        self.housing_costs += mortgage.annual_payment
        self.housing_costs = self.housing_costs.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        debug_message = f"[DEBUG] Mortgage added with annual payment {mortgage.annual_payment}."
        debug_message += f" Total housing costs now {self.housing_costs}."
        print(debug_message)

    def aggregate_income(self) -> Decimal:
        """
        Sums the incomes of all household members.

        Returns:
            Decimal: The total household income for the current period.
        """
        total_income = sum((member.income for member in self.members), Decimal("0.00"))
        total_income += self.cash_reserves  # Include windfalls
        self.cash_reserves = Decimal("0.00")  # Reset after use
        print(f"[DEBUG] Aggregated household income: {total_income}.")
        return total_income

    def aggregate_taxes(self) -> Decimal:
        """
        Sums the taxes owed by all household members.

        Returns:
            Decimal: The total taxes for the household for the current period.
        """
        total_taxes = sum((member.calculate_taxes() for member in self.members), Decimal("0.00"))
        print(f"[DEBUG] Aggregated household taxes: {total_taxes}.")
        return total_taxes

    def total_mandatory_expenses(self) -> Decimal:
        """
        Calculates the sum of all mandatory expenses, including living and housing costs.

        Returns:
            Decimal: The total mandatory expenses for the household for the current period.
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
        debug_message = f"[DEBUG] Applied inflation rate of {inflation_rate * 100}% to living and housing costs."
        print(debug_message)

    def increase_living_costs(self, amount: Decimal) -> None:
        """
        Increases the living costs by a specified amount.

        Args:
            amount (Decimal): The amount to increase living costs by.
        """
        self.living_costs += amount
        self.living_costs = self.living_costs.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        debug_message = f"[DEBUG] Living costs increased by {amount}. Total living costs now {self.living_costs}."
        print(debug_message)

    def add_windfall(self, amount: Decimal) -> None:
        """
        Adds a windfall amount to the household's cash reserves.

        Args:
            amount (Decimal): The windfall amount to add.
        """
        self.cash_reserves += amount
        self.cash_reserves = self.cash_reserves.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        debug_message = (
            f"[DEBUG] Windfall of {amount} added to cash reserves. Total cash reserves now {self.cash_reserves}."
        )
        print(debug_message)

    def get_member_by_name(self, name: str) -> Optional[Person]:
        """
        Retrieves a household member by name.

        Args:
            name (str): The name of the household member.

        Returns:
            Optional[Person]: The Person instance if found, else None.
        """
        for member in self.members:
            if member.name == name:
                return member
        return None
