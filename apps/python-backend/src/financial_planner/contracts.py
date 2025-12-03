# financial_planner/contracts.py
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from .transactions import Transaction, TransactionGenerator, TransactionTimeline
from .state import Liability

def _add_months(base_date: datetime, months: int) -> datetime:
    """
    Naive helper to increment a date by 'months' months 
    without simply adding 30*N days. 
    (Does not handle edge cases of final day in short months elegantly.)
    """
    year = base_date.year + (base_date.month - 1 + months) // 12
    month = (base_date.month - 1 + months) % 12 + 1
    day = min(base_date.day, 28)  # naive fix for edge-of-month
    return datetime(year, month, day, base_date.hour, base_date.minute, base_date.second)

class FinancialContract:
    """
    Base class for financial contracts that produce (or might produce) transactions.
    Subclasses can store references to liabilities or stateful variables as needed.
    """
    def __init__(self):
        self.cancelled = False

    def register(self, timeline: TransactionTimeline):
        raise NotImplementedError

    def cancel(self):
        self.cancelled = True

class RecurringTransactionGenerator(TransactionGenerator):
    """
    Generic recurring transaction generator. 
    If 'cancelled' is True, it stops generating further transactions.
    """
    def __init__(self, start_date: datetime, interval: timedelta, amount: Decimal,
                 category: str, end_date: datetime = None, metadata: dict = None):
        self.current_date = start_date
        self.interval = interval
        self.amount = amount.quantize(Decimal("0.01"), ROUND_HALF_UP)
        self.category = category
        self.end_date = end_date
        self.metadata = metadata or {}
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def generate(self, up_to: datetime) -> List[Transaction]:
        if self.cancelled:
            return []
        txs = []
        while self.current_date <= up_to:
            if self.end_date and self.current_date > self.end_date:
                break
            txs.append(Transaction(
                timestamp=self.current_date,
                amount=float(self.amount),
                category=self.category,
                metadata=self.metadata
            ))
            # Advance to next interval
            self.current_date += self.interval
        return txs

class EmploymentContract(FinancialContract):
    """
    Employment Contract
    -------------------
    Produces recurring salary transactions. Typically attached to a Person.
    """
    def __init__(self, start_date: datetime, salary: Decimal, interval: timedelta,
                 end_date: datetime = None, person_name: str = ""):
        super().__init__()
        self.start_date = start_date
        self.salary = salary
        self.interval = interval
        self.end_date = end_date
        self.person_name = person_name
        self.generator: Optional[RecurringTransactionGenerator] = None

    def register(self, timeline: TransactionTimeline):
        self.generator = RecurringTransactionGenerator(
            start_date=self.start_date,
            interval=self.interval,
            amount=self.salary,
            category="salary",
            end_date=self.end_date,
            metadata={"person": self.person_name}
        )
        timeline.add_generator(self.generator)

    def cancel(self):
        super().cancel()
        if self.generator:
            self.generator.cancel()

class MortgageContract(FinancialContract):
    """
    Mortgage Contract
    -----------------
    Generates recurring payments, splitting each into interest and principal.
    Also keeps a reference to a Liability so each principal repayment 
    reduces the outstanding balance automatically.
    """
    def __init__(self, start_date: datetime, principal: Decimal, annual_interest_rate: Decimal,
                 term_years: int, liability: Liability):
        super().__init__()
        self.start_date = start_date
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.term_years = term_years
        self.liability = liability
        self.generator: Optional["MortgagePaymentGenerator"] = None

    def register(self, timeline: TransactionTimeline):
        self.generator = MortgagePaymentGenerator(
            start_date=self.start_date,
            principal=self.principal,
            annual_interest_rate=self.annual_interest_rate,
            term_years=self.term_years,
            liability=self.liability
        )
        timeline.add_generator(self.generator)

    def cancel(self):
        super().cancel()
        if self.generator:
            self.generator.cancel()

class MortgagePaymentGenerator(TransactionGenerator):
    """
    Stateful generator that produces monthly mortgage payments until 
    the loan is fully paid or contract is cancelled.
    Each principal repayment reduces the attached Liability.
    """
    def __init__(self, start_date: datetime, principal: Decimal, annual_interest_rate: Decimal,
                 term_years: int, liability: Liability):
        self.current_date = start_date
        self.liability = liability
        self.annual_interest_rate = annual_interest_rate
        self.term_months = term_years * 12
        self.cancelled = False

        # Compute monthly payment using a standard annuity formula
        monthly_rate = annual_interest_rate / Decimal("12")
        if annual_interest_rate == Decimal("0"):
            self.payment = principal / Decimal(self.term_months)
        else:
            self.payment = principal * (monthly_rate * (1 + monthly_rate) ** self.term_months) / (
                (1 + monthly_rate) ** self.term_months - 1
            )
        self.payment = self.payment.quantize(Decimal("0.01"), ROUND_HALF_UP)

        self.remaining_balance = principal.quantize(Decimal("0.01"), ROUND_HALF_UP)

    def cancel(self):
        self.cancelled = True

    def generate(self, up_to: datetime) -> List[Transaction]:
        if self.cancelled or self.remaining_balance <= Decimal("0.00"):
            return []
        txs = []
        while self.current_date <= up_to and self.remaining_balance > Decimal("0.00"):
            monthly_rate = self.annual_interest_rate / Decimal("12")
            interest = (self.remaining_balance * monthly_rate).quantize(Decimal("0.01"), ROUND_HALF_UP)
            principal_payment = self.payment - interest
            if principal_payment > self.remaining_balance:
                principal_payment = self.remaining_balance

            # Create two transactions
            txs.append(Transaction(self.current_date, -float(interest), "mortgage_interest", {"type": "mortgage"}))
            txs.append(Transaction(self.current_date, -float(principal_payment), "mortgage_principal", {"type": "mortgage"}))

            # Reduce the liability's outstanding balance
            self.liability.reduce_balance(principal_payment)

            self.remaining_balance -= principal_payment
            self.remaining_balance = self.remaining_balance.quantize(Decimal("0.01"), ROUND_HALF_UP)

            # Advance to next monthly date (more precise than +30 days)
            self.current_date = _add_months(self.current_date, 1)

            if self.cancelled:
                break
        return txs

class RentContract(FinancialContract):
    """
    Rent Contract
    ------------
    Generates recurring rent payments (negative outflow).
    """
    def __init__(self, start_date: datetime, monthly_rent: Decimal, end_date: datetime = None):
        super().__init__()
        self.start_date = start_date
        # For an expense, the amount is negative.
        self.monthly_rent = -abs(monthly_rent)
        self.end_date = end_date
        self.generator: Optional[RecurringTransactionGenerator] = None

    def register(self, timeline: TransactionTimeline):
        self.generator = RecurringTransactionGenerator(
            start_date=self.start_date,
            interval=timedelta(days=30),  # or use a monthly helper if needed
            amount=self.monthly_rent,
            category="rent",
            end_date=self.end_date
        )
        timeline.add_generator(self.generator)

    def cancel(self):
        super().cancel()
        if self.generator:
            self.generator.cancel()
