# financial_planner/events/__init__.py
from typing import Type, Dict, Any

EVENT_REGISTRY: Dict[str, Type["EventBase"]] = {}


def register_event_type(name: str, cls: Type["EventBase"]) -> None:
    """
    Registers an event class under the given name in the EVENT_REGISTRY.
    """
    EVENT_REGISTRY[name] = cls


class EventBase:
    """
    Base class for all one-shot (non-repeating) events. Subclasses must implement apply().
    """

    def __init__(self, event_datetime, **kwargs):
        """
        Args:
            event_datetime: A Python datetime or something comparable.
            **kwargs: Other fields from the config.
        """
        self.event_datetime = event_datetime
        self.triggered = False  # Once triggered, stays triggered (for one-shot events).
        self.event_data = kwargs

    def apply(self, household, current_time) -> None:
        """
        Apply the event’s logic to the household. Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement apply().")

    def should_trigger(self, current_time) -> bool:
        """
        Determines if the event is due to be triggered at 'current_time'.
        """
        return (not self.triggered) and (current_time >= self.event_datetime)
