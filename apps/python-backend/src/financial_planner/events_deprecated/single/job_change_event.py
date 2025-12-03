# financial_planner/events/job_change_event.py
from decimal import Decimal
from datetime import datetime
from .. import EventBase, register_event_type

class JobChangeEvent(EventBase):
    """
    Updates a member's income at a specific time.
    """

    # Should be delete job, add new job

    def __init__(self, event_datetime: datetime, member_name: str, new_income: float, **kwargs):
        super().__init__(event_datetime=event_datetime, **kwargs)
        self.member_name = member_name
        self.new_income = Decimal(str(new_income))

    def apply(self, household, current_time: datetime) -> None:
        member = household.get_member_by_name(self.member_name)
        if member:
            member.update_income_specific(self.new_income) 
        else:
            print(f"[WARNING] Member '{self.member_name}' not found.")
        self.triggered = True

register_event_type("job_change", JobChangeEvent)
