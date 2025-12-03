# financial_planner/events.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any
from decimal import Decimal

from .contracts import MortgageContract, EmploymentContract, RentContract
from .state import Asset, Liability
from .transactions import Transaction
from .household import Household

class SimulationContext:
    """
    Provides the current time and the aggregator(s) we want to modify. 
    Typically, an event changes the Household or a Person inside it.
    """
    def __init__(self, current_time: datetime, household: Household):
        self.current_time = current_time
        self.household = household

class EventBase(ABC):
    """
    Base class for simulation events. 
    They decide how to apply themselves to the Household or Persons.
    """
    def __init__(self, event_time: datetime, data: Dict[str, Any]):
        self.event_time = event_time
        self.data = data

    @abstractmethod
    def apply(self, context: SimulationContext):
        pass

class MortgagePurchaseEvent(EventBase):
    """
    Buys a house, registers a MortgageContract, adds a liability and an asset.
    """
    def apply(self, context: SimulationContext):
        principal = Decimal(str(self.data["principal"]))
        interest_rate = Decimal(str(self.data["interest_rate"]))
        term_years = int(self.data.get("term_years", 30))

        # Create a Liability
        mortgage_liability = Liability("Mortgage", principal)
        # Create an Asset
        house_asset = Asset("House", principal, self.event_time)

        # Register mortgage contract, linking the liability
        contract = MortgageContract(
            start_date=self.event_time,
            principal=principal,
            annual_interest_rate=interest_rate,
            term_years=term_years,
            liability=mortgage_liability
        )

        context.household.add_liability(mortgage_liability)
        context.household.add_asset(house_asset)
        context.household.add_contract(contract)

class WindfallEvent(EventBase):
    """
    Immediate one-off cash inflow on the household timeline.
    """
    def apply(self, context: SimulationContext):
        amount = Decimal(str(self.data["amount"]))
        tx = Transaction(timestamp=self.event_time, amount=float(amount), category="windfall",
                         metadata={"description": "Windfall"})
        context.household.timeline.add_transaction(tx)

class EmploymentChangeEvent(EventBase):
    """
    Adds a new employment contract to a specified person. 
    Optionally cancels the old contract if desired.
    """
    def apply(self, context: SimulationContext):
        person_name = self.data["person_name"]
        salary = Decimal(str(self.data["new_salary"]))
        interval_days = int(self.data.get("interval_days", 30))

        # Find the Person in the household
        target_person = None
        for member in context.household.members:
            if member.name == person_name:
                target_person = member
                break

        if not target_person:
            return  # person not found

        # Potentially you might look up an existing EmploymentContract and cancel it
        # For now, we just add a new one
        from datetime import timedelta
        new_contract = EmploymentContract(
            start_date=self.event_time,
            salary=salary,
            interval=timedelta(days=interval_days),
            person_name=person_name
        )
        target_person.add_contract(new_contract)

class NewChildEvent(EventBase):
    """
    Adds a large new child expense as a direct transaction, or 
    modifies household living costs, etc.
    """
    def apply(self, context: SimulationContext):
        expense = Decimal("5000.00")
        tx = Transaction(timestamp=self.event_time, amount=float(-expense), category="child_expense",
                         metadata={"description": "New Child"})
        context.household.timeline.add_transaction(tx)
