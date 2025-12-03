# financial_planner/events/house_purchase_event.py
from decimal import Decimal
from datetime import datetime
from .. import EventBase, register_event_type
from ...household import Mortgage

class HousePurchaseEvent(EventBase):
    """
    One-shot event. Creates a mortgage in the household at the scheduled time.
    """

    def __init__(self, event_datetime: datetime, principal: float, interest_rate: float, **kwargs):
        super().__init__(event_datetime=event_datetime, **kwargs)
        self.principal = Decimal(str(principal))
        self.interest_rate = Decimal(str(interest_rate))

    def apply(self, household, current_time: datetime) -> None:
        mortgage = Mortgage(principal=self.principal, interest_rate=self.interest_rate)
        household.add_mortgage(mortgage) # This should be liability
        # Should add asset here
        self.triggered = True

register_event_type("house_purchase", HousePurchaseEvent)

