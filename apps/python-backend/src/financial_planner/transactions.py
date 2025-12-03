# financial_planner/transactions.py
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class Transaction:
    """
    Atomic Transaction
    ------------------
    The smallest unit of monetary movement.
      - timestamp: When the event occurs.
      - amount: Positive for inflows, negative for outflows.
      - category: E.g. 'salary', 'expense', 'mortgage_principal', etc.
      - metadata: Arbitrary details (e.g. 'person': 'Alice', 'description': 'windfall').
    """
    def __init__(self, timestamp: datetime, amount: float, category: str, metadata: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.amount = amount
        self.category = category
        self.metadata = metadata or {}

    def __repr__(self):
        return f"Transaction({self.timestamp.isoformat()}, {self.amount}, {self.category})"


class TransactionGenerator(ABC):
    """
    Interface for objects that generate transactions over time.
    Each generator maintains its own state, so re-running from the start
    generally requires a fresh generator object.
    """
    @abstractmethod
    def generate(self, up_to: datetime) -> List[Transaction]:
        pass

    @abstractmethod
    def cancel(self):
        """
        Optional: Provide a way to cancel or stop generating future transactions.
        """
        pass


class TransactionTimeline:
    """
    Transaction Timeline (Event Container)
    --------------------------------------
    Holds both ad hoc transactions and rule-generated transactions.
    """
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.generators: List[TransactionGenerator] = []

    def add_transaction(self, tx: Transaction):
        self.transactions.append(tx)

    def add_generator(self, generator: TransactionGenerator):
        self.generators.append(generator)

    def remove_generator(self, generator: TransactionGenerator):
        """
        If needed, remove a generator entirely from the timeline.
        """
        if generator in self.generators:
            self.generators.remove(generator)

    def generate_transactions(self, up_to: datetime):
        """
        For each generator, produce any new transactions up to 'up_to'
        and store them. If a generator is cancelled or exhausted, it
        simply won't produce more.
        """
        for generator in self.generators:
            new_txs = generator.generate(up_to)
            self.transactions.extend(new_txs)

    def get_transactions(self, start_time: datetime = None, end_time: datetime = None) -> List[Transaction]:
        txs = self.transactions
        if start_time:
            txs = [tx for tx in txs if tx.timestamp >= start_time]
        if end_time:
            txs = [tx for tx in txs if tx.timestamp <= end_time]
        return sorted(txs, key=lambda tx: tx.timestamp)
