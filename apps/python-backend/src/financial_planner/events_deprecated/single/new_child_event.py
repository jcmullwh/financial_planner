# financial_planner/events/new_child_event.py
from decimal import Decimal
from datetime import datetime
from .. import EventBase, register_event_type

class NewChildEvent(EventBase):
    """
    Increases living costs by a fixed amount, once.
    """
# Should be add person
    def __init__(self, event_datetime: datetime, added_cost: float = 5000.00, **kwargs):
        super().__init__(event_datetime=event_datetime, **kwargs)
        self.added_cost = Decimal(str(added_cost))

    def apply(self, household, current_time: datetime) -> None:
        household.increase_living_costs(self.added_cost)
        self.triggered = True

register_event_type("new_child", NewChildEvent)
