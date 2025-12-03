# financial_planner/household.py
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import List

from .person import Person
from .transactions import TransactionTimeline, Transaction
from .contracts import FinancialContract
from .state import Asset, Liability

class Household:
    """
    Household Aggregator
    --------------------
    Combines multiple Person objects plus any household-level 
    contracts, assets, liabilities, and a Household-level timeline.
    """
    def __init__(self):
        self.members: List[Person] = []
        self.timeline = TransactionTimeline()
        self.contracts: List[FinancialContract] = []
        self.assets: List[Asset] = []
        self.liabilities: List[Liability] = []

    def add_member(self, person: Person):
        self.members.append(person)

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
        """
        Combine household-level timeline transactions plus all member transactions.
        """
        all_txs = self.timeline.get_transactions(start_time, end_time)
        for member in self.members:
            all_txs.extend(member.aggregate_transactions(start_time, end_time))
        return sorted(all_txs, key=lambda tx: tx.timestamp)

    def total_income(self, start_time: datetime, end_time: datetime) -> Decimal:
        txs = self.aggregate_transactions(start_time, end_time)
        amt = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount > 0)
        return amt.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def total_expenses(self, start_time: datetime, end_time: datetime) -> Decimal:
        txs = self.aggregate_transactions(start_time, end_time)
        amt = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount < 0)
        return amt.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def compute_net_worth(self) -> Decimal:
        """
        Summation of this Household's assets & liabilities plus the sum of each member's net worth.
        """
        assets_value = sum(a.current_value for a in self.assets)
        liabilities_value = sum(l.outstanding_balance for l in self.liabilities)
        for member in self.members:
            assets_value += sum(a.current_value for a in member.assets)
            liabilities_value += sum(l.outstanding_balance for l in member.liabilities)
        net = (assets_value - liabilities_value).quantize(Decimal("0.01"), ROUND_HALF_UP)
        return net
