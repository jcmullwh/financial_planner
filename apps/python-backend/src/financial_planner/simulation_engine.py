# financial_planner/simulation_engine.py
from datetime import datetime, timedelta
from typing import List
from .events import EventBase, SimulationContext
from .household import Household
from decimal import Decimal

class SimulationEngine:
    """
    Simulation Engine
    -----------------
    Iterates through time in increments of 'time_step', 
    applies relevant events, triggers transaction generation, 
    and records snapshots. 
    Now handles mid-step events by checking event times within 
    (current_time, next_time].
    """
    def __init__(self, start_time: datetime, end_time: datetime, time_step: timedelta):
        self.start_time = start_time
        self.end_time = end_time
        self.time_step = time_step
        self.current_time = start_time

        self.household = Household()
        self.events: List[EventBase] = []
        self.results = []

    def add_event(self, event: EventBase):
        self.events.append(event)

    def run(self):
        """
        Runs the simulation from start_time to end_time. 
        In each loop:
          1. Determine the next time step
          2. Apply any events between current_time and next_time (excl. current_time, incl. next_time)
          3. Generate transactions up to next_time
          4. Store a snapshot
          5. Move current_time -> next_time
        """
        while self.current_time <= self.end_time:
            next_time = self.current_time + self.time_step
            if next_time > self.end_time:
                next_time = self.end_time

            # Apply events that lie within (current_time, next_time]
            context = SimulationContext(current_time=self.current_time, household=self.household)
            for evt in self.events:
                if self.current_time < evt.event_time <= next_time:
                    evt.apply(context)

            # Generate transactions up to next_time
            self.household.timeline.generate_transactions(next_time)
            for member in self.household.members:
                member.timeline.generate_transactions(next_time)

            # Record state snapshot at next_time
            self._record_state_snapshot(next_time)

            # Advance time
            if next_time == self.end_time:
                break
            self.current_time = next_time

    def _record_state_snapshot(self, snapshot_time: datetime):
        txs = self.household.aggregate_transactions(self.start_time, snapshot_time)
        income = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount > 0)
        expenses = sum(Decimal(str(tx.amount)) for tx in txs if tx.amount < 0)
        net = (income + expenses).quantize(Decimal("0.01"))

        snapshot = {
            "time": snapshot_time,
            "income": income,
            "expenses": expenses,
            "net": net,
            "household_net_worth": self.household.compute_net_worth()
        }
        self.results.append(snapshot)
