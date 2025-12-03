# financial_planner/events/windfall_event.py
from decimal import Decimal
from datetime import datetime
from .. import EventBase, register_event_type

class WindfallEvent(EventBase):
    """
    Adds a lump-sum amount to the household's cash reserves at the scheduled time.
    """

    def __init__(self, event_datetime: datetime, amount: float, **kwargs):
        super().__init__(event_datetime=event_datetime, **kwargs)
        self.amount = Decimal(str(amount))

    def apply(self, household, current_time: datetime) -> None:
        household.add_windfall(self.amount) # should be add inflow or income
        self.triggered = True

register_event_type("windfall", WindfallEvent)
