# financial_planner/person.py
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import List

from .transactions import TransactionTimeline, Transaction
from .contracts import FinancialContract
from .state import Asset, Liability

class Person:
    """
    Person Aggregator
    -----------------
    Aggregates that individual's:
      - TransactionTimeline
      - Contracts (e.g. EmploymentContract)
      - Assets, Liabilities, etc.
    """
    def __init__(self, name: str):
        self.name = name
        self.timeline = TransactionTimeline()
        self.contracts: List[FinancialContract] = []
        self.assets: List[Asset] = []
        self.liabilities: List[Liability] = []

    def add_contract(self, contract: FinancialContract):
        self.contracts.append(contract)
        contract.register(self.timeline)

    def remove_contract(self, contract: FinancialContract):
        if contract in self.contracts:
            contract.cancel()
            self.contracts.remove(contract)

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def add_liability(self, liability: Liability):
        self.liabilities.append(liability)

    def aggregate_transactions(self, start_time: datetime, end_time: datetime) -> List[Transaction]:
        return self.timeline.get_transactions(start_time, end_time)

    def total_income(self, start_time: datetime, end_time: datetime) -> Decimal:
        txs = self.aggregate_transactions(start_time, end_time)
        amt = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount > 0)
        return amt.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def total_expenses(self, start_time: datetime, end_time: datetime) -> Decimal:
        txs = self.aggregate_transactions(start_time, end_time)
        amt = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount < 0)
        return amt.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def compute_net_worth(self) -> Decimal:
        assets_value = sum(asset.current_value for asset in self.assets)
        liabilities_value = sum(liab.outstanding_balance for liab in self.liabilities)
        return (assets_value - liabilities_value).quantize(Decimal("0.01"), ROUND_HALF_UP)
