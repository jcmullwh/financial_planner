# financial_planner/simulation_engine.py

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Optional

from .config_loader import validate_event
from .household import Household, Mortgage
from .person import Person


class SimulationEngine:
    """
    Coordinates the simulation by managing the household, iterating through each simulation period,
    updating financial states, applying events, and generating reports based on the simulation results.
    """

    def __init__(self) -> None:
        """
        Initializes a SimulationEngine instance.
        """
        self.config: Optional[dict] = None
        self.household: Optional[Household] = None
        self.start_year: Optional[int] = None
        self.end_year: Optional[int] = None
        self.inflation_rate: Decimal = Decimal("0.00")
        self.results: list[dict[str, Decimal]] = []
        self.events: list[dict[str, Any]] = []
        self.time_frequency: str = "YEAR"  # Default frequency

    def load_scenario(self, config: dict) -> None:
        """
        Reads and parses the scenario configuration to initialize simulation parameters
        and household details.

        Args:
            config (Dict): A dictionary representing the parsed configuration file.

        Raises:
            ValueError: If required fields are missing or have invalid values.
        """
        try:
            self.start_year = int(config["start_year"])
            self.end_year = int(config["end_year"])
            self.inflation_rate = Decimal(str(config.get("inflation_rate", 0.0))).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

            # Handle time_frequency for future iterations
            self.time_frequency = config.get("time_frequency", "YEAR").upper()
            if self.time_frequency not in {"YEAR", "MONTH", "DAY"}:
                error_message = f"Invalid time_frequency: {self.time_frequency}. Must be YEAR, MONTH, or DAY."
                raise ValueError(error_message)

            household_config = config["household"]
            living_costs = float(household_config["living_costs"])
            housing_costs = float(household_config["housing_costs"])
            members_config = household_config["members"]

            members = []
            for member in members_config:
                name = member["name"]
                income = float(member["income"])
                tax_rate = float(member["tax_rate"])
                savings = float(member.get("savings", 0.0))
                members.append(Person(name=name, income=income, tax_rate=tax_rate, savings=savings))

            self.household = Household(members=members, living_costs=living_costs, housing_costs=housing_costs)

            # Parse events if present
            self.events = config.get("events", [])
            for event in self.events:
                validate_event(event)

            print("[DEBUG] Scenario loaded successfully.")

        except KeyError as e:
            error_message = f"Missing required configuration field: {e}"
            raise ValueError(error_message) from e
        except (TypeError, ValueError) as e:
            error_message = f"Invalid configuration value: {e}"
            raise ValueError(error_message) from e
        
    def store_config(self, config: dict) -> None:
            """
            Stores the configuration for the simulation engine.

            Args:
                config (dict): The configuration dictionary to store.
            """
            self.config = config
            print("[DEBUG] Configuration stored.")

    def apply_event(self, event: dict) -> None:
        """
        Applies an event to the household based on its type.

        Args:
            event (dict): The event dictionary containing event details.
        """
        event_type = event["type"]
        year = event["year"]

        print(f"[DEBUG] Applying event '{event_type}' for year {year}.")

        if self.household is None:
            error_message = "Household not initialized."
            raise RuntimeError(error_message)

        if event_type == "house_purchase":
            principal = Decimal(str(event["principal"]))
            interest_rate = Decimal(str(event["interest_rate"]))
            mortgage = Mortgage(principal=principal, interest_rate=interest_rate)
            self.household.add_mortgage(mortgage)
            print(f"[DEBUG] Mortgage added: Principal={principal}, Interest Rate={interest_rate}")

        elif event_type == "new_child":
            additional_expense = Decimal("5000.00")  # Example fixed increase
            self.household.increase_living_costs(additional_expense)
            print(f"[DEBUG] Living costs increased by {additional_expense} due to new child.")

        elif event_type == "job_change":
            member_name = event["member_name"]
            new_income = Decimal(str(event["new_income"]))
            member = self.household.get_member_by_name(member_name)
            if member:
                member.update_income_specific(new_income)
                print(f"[DEBUG] {member_name}'s income updated to {new_income}.")
            else:
                print(f"[WARNING] Member '{member_name}' not found in household.")

        elif event_type == "windfall":
            amount = Decimal(str(event["amount"]))
            self.household.add_windfall(amount)
            print(f"[DEBUG] Windfall of {amount} added to household.")

    def run_simulation(self) -> None:
        """
        Executes the multi-period financial loop, updating incomes, calculating taxes and expenses,
        applying events, and determining naive discretionary income for each period.
        """
        if self.household is None:
            error_message = "Household not initialized."
            raise RuntimeError(error_message)
        if self.start_year is None or self.end_year is None:
            error_message = "Invalid simulation boundaries."
            raise RuntimeError(error_message)

        # Reset results at the beginning of the simulation
        self.results = []

        current_period = self.start_year
        print(f"[DEBUG] Period is currently {current_period}.")
        self.calculate_and_store_results(current_period)

        while current_period < self.end_year:
            self.update_period(current_period)
            current_period += 1
            print(f"[DEBUG] Period is currently {current_period}.")
            self.calculate_and_store_results(current_period)

    def update_period(self, period: int) -> None:
        """
        Apply all modifications that 'move time forward' to the household,
        such as inflation, income updates, and event handling.
        """
        if self.household is None:
            error_message = "Household not initialized."
            raise RuntimeError(error_message)
        if self.start_year is None:
            error_message = "Start year not defined."
            raise RuntimeError(error_message)

        print("[DEBUG] Moving to next period.")

        # Apply inflation only after the first period
        if period >= self.start_year and self.inflation_rate > Decimal("0.00"):
            self.household.apply_inflation(float(self.inflation_rate))

        # Update incomes
        for member in self.household.members:
            member.update_income(period + 1)

        # Apply events for the period
        next_period_events = [e for e in self.events if e["year"] == period]
        for event in next_period_events:
            self.apply_event(event)

    def calculate_and_store_results(self, period: int) -> None:
        """
        Aggregates and stores financial data (incomes, taxes, leftover) for the given period.
        """
        if self.household is None:
            error_message = "Household not initialized."
            raise RuntimeError(error_message)

        total_income = self.household.aggregate_income()
        total_taxes = self.household.aggregate_taxes()
        total_mandatory_expenses = self.household.total_mandatory_expenses()
        leftover = (total_income - total_taxes - total_mandatory_expenses).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        year_result = {
            "year": Decimal(period),
            "total_income": total_income,
            "total_taxes": total_taxes,
            "total_mandatory_expenses": total_mandatory_expenses,
            "leftover": leftover,
            "naive_discretionary": leftover,
            "living_costs": self.household.living_costs,
            "housing_costs": self.household.housing_costs,
        }
        self.results.append(year_result)
