# financial_planner/state.py
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class Asset:
    """
    Asset
    -----
    Represents a resource of value that may change over time.
    current_value can be updated by events or revaluation logic.
    """
    def __init__(self, name: str, acquisition_value: Decimal, acquisition_date: datetime):
        self.name = name
        self.acquisition_value = acquisition_value.quantize(Decimal("0.01"), ROUND_HALF_UP)
        self.acquisition_date = acquisition_date
        self.current_value = self.acquisition_value

    def update_market_value(self, new_value: Decimal):
        self.current_value = new_value.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def equity(self, related_liabilities: Decimal = Decimal("0.00")) -> Decimal:
        return (self.current_value - related_liabilities).quantize(Decimal("0.01"), ROUND_HALF_UP)

class Liability:
    """
    Liability
    ---------
    Represents an obligation that is reduced over time by principal repayments.
    """
    def __init__(self, name: str, initial_amount: Decimal):
        self.name = name
        self.outstanding_balance = initial_amount.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def reduce_balance(self, amount: Decimal):
        self.outstanding_balance -= amount.quantize(Decimal("0.01"), ROUND_HALF_UP)
        if self.outstanding_balance < Decimal("0.00"):
            self.outstanding_balance = Decimal("0.00")
