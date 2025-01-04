# Architecture Overview

A bird’s-eye view of the system’s primary components and data flows.

## 1. Core Components

### SimulationEngine

- Manages the yearly simulation loop.
- Loads scenario data (like time span, inflation rate, etc.).
- Updates incomes, applies events, calculates taxes, and tracks results.

### Household

- Aggregates multiple Person objects.
- Manages shared costs (living_costs, housing_costs).
- Summarizes total income and total taxes across members.

### Person

- Represents an individual’s financial data (income, tax_rate, etc.).
- Methods for updating income or calculating taxes.

### Scenario Config

- YAML/JSON file describing your time horizon, household details, inflation, etc.

### Reference Docs

- Auto-generated from docstrings for classes and methods.

## 2. Data Flow

### Scenario Loading

`SimulationEngine.load_scenario()` reads a YAML or JSON file and creates a Household object with Person instances.

### Yearly Simulation

For each year from `start_year` to `end_year`:
- Update each Person’s income (if growth logic is applied).
- Aggregate income and taxes.
- Subtract mandatory expenses (living_costs, housing_costs), adjusted by inflation_rate.
- Record leftover, naive discretionary, and any relevant data.

### Output

Results are stored internally and optionally written to a CSV file or displayed in the console.

## 3. Key Advantages

- **Modular**: Each class focuses on one role—makes it easier to extend or swap logic.
- **Scenario-Based**: Users can define multiple scenario files to compare outcomes (like different inflation assumptions or household compositions).
- **Extensible**: Start with simple tax logic, then add bracket-based or local laws over time.

## 4. Future Directions

- **Complex Tax Modules**: Incorporate bracket systems, deductions, credits, etc.
- **Event Handling**: Handle major life changes (e.g., new child, mortgage, job switch).
- **Discretionary Models**: Implement more sophisticated approaches to leftover distribution.
- **User Interface**: Develop a GUI or web app front-end for non-technical users.

## 5. Key Advantages

- **Modular Design**: Facilitates easy maintenance and future expansions.
- **Scenario Flexibility**: Allows users to test various financial situations without altering the core code.
- **Extensible**: The architecture supports adding more complex financial models and features as needed.

## 6. Conclusion

The Architecture Overview provides a high-level understanding of how the system's components interact to perform financial simulations. This structure ensures that the system is both robust and adaptable, ready to incorporate more advanced features in the future without compromising existing functionality.

For a deeper dive into specific design decisions, refer to the Design Choices document.