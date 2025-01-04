# financial_planner/simulation_engine.py

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from .household import Household


class SimulationEngine:
    """
    Coordinates the simulation by managing the household, iterating through each simulation year,
    updating financial states, and generating reports based on the simulation results.
    """

    def __init__(self) -> None:
        """
        Initializes a SimulationEngine instance.
        """
        self.household: Optional[Household] = None
        self.start_year: Optional[int] = None
        self.end_year: Optional[int] = None
        self.inflation_rate: Decimal = Decimal("0.00")
        self.results: list[dict[str, Decimal]] = []

    def load_scenario(self, config: dict) -> None:
        """
        Reads and parses the basic scenario configuration to initialize simulation parameters
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

            household_config = config["household"]
            living_costs = float(household_config["living_costs"])
            housing_costs = float(household_config["housing_costs"])
            members_config = household_config["members"]

            from .person import Person  # Importing here to avoid circular imports

            members = []
            for member in members_config:
                name = member["name"]
                income = float(member["income"])
                tax_rate = float(member["tax_rate"])
                savings = float(member.get("savings", 0.0))
                members.append(Person(name=name, income=income, tax_rate=tax_rate, savings=savings))

            self.household = Household(members=members, living_costs=living_costs, housing_costs=housing_costs)

            print("[DEBUG] Scenario loaded successfully.")

        except KeyError as e:
            message = f"Missing required configuration field: {e}"
            raise ValueError(message) from e
        except (TypeError, ValueError) as e:
            message = f"Invalid configuration value: {e}"
            raise ValueError(message) from e

    def run_simulation(self) -> None:
        """
        Executes the multi-year financial loop, updating incomes, calculating taxes and expenses,
        and determining naive discretionary income for each year.
        """
        if not self.household or self.start_year is None or self.end_year is None:
            message = "SimulationEngine is not properly initialized. Please load a scenario first."
            raise RuntimeError(message)

        for year in range(self.start_year, self.end_year + 1):
            print(f"[DEBUG] Running simulation for year {year}.")

            # Update incomes
            for member in self.household.members:
                member.update_income(year)

            # Calculate total income
            total_income = self.household.aggregate_income()

            # Calculate total taxes
            total_taxes = self.household.aggregate_taxes()

            # Calculate total mandatory expenses
            total_mandatory_expenses = self.household.total_mandatory_expenses()

            # Determine leftover income
            leftover = (total_income - total_taxes - total_mandatory_expenses).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            naive_discretionary = leftover  # At this stage, no savings allocation

            # Capture current expenses before applying inflation
            current_living_costs = self.household.living_costs
            current_housing_costs = self.household.housing_costs

            # Store results
            year_result = {
                "year": Decimal(year),
                "total_income": total_income,
                "total_taxes": total_taxes,
                "total_mandatory_expenses": total_mandatory_expenses,
                "leftover": leftover,
                "naive_discretionary": naive_discretionary,
                "living_costs": current_living_costs,
                "housing_costs": current_housing_costs,
            }
            self.results.append(year_result)

            print(f"[DEBUG] Year {year} results: {year_result}")

            # Apply inflation to next year's expenses if not the last year
            if self.inflation_rate > Decimal("0.00") and year < self.end_year:
                self.household.apply_inflation(float(self.inflation_rate))
