from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

class CostItemBase(ABC):
    """
    Abstract base for cost items. Each subclass can handle its own inflation logic
    and cost calculation over time.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def update_costs(self, inflation_rate: Decimal) -> None:
        """
        Adjust this cost item’s amounts according to inflation or other logic.
        """
        pass

    @abstractmethod
    def get_period_cost(self, current_time: datetime) -> Decimal:
        """
        Returns the cost for the current time step (annual, monthly, etc.).
        """
        pass


class MortgageCostItem(CostItemBase):
    """
    A cost item that reflects a mortgage payment each year (or partial period).
    For simplicity, we’ll keep it annual as your code does.
    """
    def __init__(self, name: str, principal: Decimal, interest_rate: Decimal, term_years: int = 30):
        super().__init__(name)
        self.principal = principal
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.remaining_balance = principal
        self.annual_payment = self._calculate_annual_payment()

    def _calculate_annual_payment(self) -> Decimal:
        rate = self.interest_rate
        n = self.term_years
        if rate == Decimal("0.0"):
            payment = self.principal / Decimal(n)
        else:
            payment = self.principal * (rate * (Decimal("1") + rate) ** n) / ((Decimal("1") + rate) ** n - Decimal("1"))
        return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def update_costs(self, inflation_rate: Decimal) -> None:
        """
        Mortgage does not inflate by default. If your logic demands variable interest,
        you could recalc or skip.
        """
        pass

    def get_period_cost(self, current_time: datetime) -> Decimal:
        """
        The cost for this year’s mortgage payment.
        """
        return self.annual_payment


class RentCostItem(CostItemBase):
    """
    Simple rent item that applies inflation each year.
    """
    def __init__(self, name: str, monthly_rent: Decimal):
        super().__init__(name)
        self.monthly_rent = monthly_rent

    def update_costs(self, inflation_rate: Decimal) -> None:
        """
        Multiply monthly rent by (1 + inflation_rate).
        """
        self.monthly_rent = (self.monthly_rent * (Decimal("1") + inflation_rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def get_period_cost(self, current_time: datetime) -> Decimal:
        # If your simulation increments yearly, return monthly_rent * 12
        return (self.monthly_rent * Decimal("12")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
