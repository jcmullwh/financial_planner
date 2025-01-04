# Project Overview

## 1. Introduction and Purpose

### What is this tool?
A multi-year financial planning system that helps individuals or households forecast and plan their finances. It models factors like incomes, taxes, expenses, savings, and discretionary spending across many years.

### Why are we building it?
- **Decision-Making**: Users can compare scenarios (e.g., buy a house in year X, or wait until year Y) and see the long-term outcomes.
- **Balancing Present vs. Future**: It helps find a middle ground between enjoying life today and ensuring enough savings for retirement or other goals.
- **Flexibility**: Different households have unique circumstances and strategies. The system can accommodate various discretionary spending rules, tax complexities, or life events.

### Who is it for?
- Financial planners or individual households wanting to test “what-if” scenarios over a 10-, 20-, or 30-year horizon (or longer).
- Non-technical individuals might rely on a user interface built on top of this core model, but the plan here is about the underlying architecture and roadmap.

### What are we not doing in detail here?
- This documentation does not provide code, nor does it detail user-interface design.
- It does not specify every possible financial complexity (like very localized tax laws or specialized investment vehicles). Instead, it offers an extensible framework to add or adapt such details.

## 2. Potential Misunderstandings and Clarifications

### Is This Only About Discretionary Spending?
No. While discretionary spending is a key component (deciding how much is “fun money” each year), the tool covers a wide range of financial elements: incomes, taxes, mortgages, savings, etc. Discretionary is just one (important) part of the puzzle.

### Is This a Spreadsheet Tool?
No. Although some ideas originated from a spreadsheet approach, the plan describes a standalone software architecture (likely in Python or a similar language). No spreadsheet software is required.

### Is This an Automated “Advice” Tool or a Calculator?
It’s a Modeling/Planning Tool. It doesn’t automatically guarantee the best outcome for every user. Instead, it provides scenarios and projections so that users (or financial professionals) can make informed decisions.

### Does It Include Real-Time Market Data?
By default, no. Market or economic data (e.g., inflation rates, investment returns) are inputs you provide as assumptions. The system does not automatically fetch or update them.

### What If My Tax System Is Different?
The plan includes a TaxModel module that is meant to be adapted to local or advanced rules. You can start with a simplified approach (flat tax, single bracket) and later implement a detailed set of rules. The architecture is flexible enough to handle that evolution.

### Is This a Turnkey Product?
No. This is an implementation roadmap. Actual code, testing, and potential UI or integration with external data are separate tasks.

## 3. Key Concepts and Architecture

Below is an overview of the system’s components and how they interact. These are modular pieces that can be combined or replaced as needs evolve.

### 3.1 Entities

#### Person
- Stores income details, potential job changes, retirement accounts, etc.
- Might represent Jason, Linda, or other earners in the household.

#### Household
- Aggregates Person objects and shared expenses (e.g., housing, family living costs).
- Handles college savings, emergency funds, or joint taxes.

#### Mortgage / Loan
- Tracks principal, interest, and payments for any property or large purchase.
- Used when a scenario includes buying a home or other big-ticket item.

#### TaxModel
- Encapsulates how taxes are calculated (from simple to complex).
- For instance, a bracket-based approach, child credits, or local surcharges if needed.

#### Scenario
- A structured input (like a YAML/JSON file) specifying the time horizon, annual events (buying a house in 2025, child birth in 2028, etc.), inflation rates, rules for discretionary spending, etc.

#### SimulationEngine
- The coordinator that runs the scenario year by year.
- For each year: update incomes, apply events, compute taxes, handle savings, and determine discretionary spending following the user-selected approach.

### 3.2 Discretionary Spending: Multiple Approaches
- **Leftover-Based**: Discretionary = leftover after mandatory expenses and savings.
- **Rule-Based**: Each year’s discretionary might grow or shrink by a certain percentage, or be bounded by min/max amounts.
- **Optimization**: A solver enforces constraints (e.g., “annual growth in discretionary can’t exceed 7%,” “final retirement must exceed $X,” etc.) and finds the best path.

#### Why the flexibility?
Different users and financial philosophies. Some want to maximize leftover each year. Others prefer to smooth discretionary so there are no abrupt changes in lifestyle.

## 4. Detailed Roadmap (Step by Step)

### 4.1 Phase 1: Foundations – Multi-Year Loop (Deterministic)

#### Purpose
Construct the basic skeleton of a multi-year financial simulation. Start simple: no complex discretionary logic or life events yet.

#### Tasks
- Implement Classes: Person, Household, SimulationEngine.
- Basic Scenario Config: A file or object with start_year, end_year, possibly an inflation rate.
- Yearly Iteration:
    - Update each Person’s income for that year (a fixed or formulaic approach).
    - Compute taxes (could be a single rate for now).
    - Subtract living and housing costs.
    - Remainder is “naive discretionary” (e.g., leftover after a simple mandatory saving if desired).

#### Potential Pitfalls / Misconceptions
- Someone might assume the tool is already final. Clarify it’s a basic prototype, only a single pass with no advanced logic.
- “Where do I input my mortgage details?” – Not yet. Mortgages come in a later phase.

#### Success Criteria
We can produce a simple table of results for each year: incomes, taxes, leftover, naive discretionary.

### 4.2 Phase 2: Events & Scenario Expansion

#### Purpose
Support major life changes like house purchases, births, job changes, or unexpected windfalls.

#### Tasks
- Scenario File: e.g., `scenarios/default.yaml` describing events:
    ```yaml
    events:
        - year: 2025
            type: 'house_purchase'
            principal: 300000
            interest_rate: 0.04
        - year: 2028
            type: 'new_child'
    ```
- Simulation Updates: In `SimulationEngine.run()`, if `year == event.year`, apply that event’s changes (e.g., create a Mortgage, add child expenses, etc.).

#### Potential Pitfalls / Misconceptions
Readers might think all scenarios must include a mortgage. Clarify that events are optional. If the user sets no events, the model simply runs with baseline assumptions.

#### Success Criteria
If an event is triggered, the system changes finances accordingly (e.g., new monthly mortgage payment after purchase year). The final ledger shows the ongoing cost of that event in subsequent years.

### 4.3 Phase 3: Discretionary Methods – Single-Year Focus

#### Purpose
Introduce alternate ways to define or calculate discretionary in each year, but not yet across multiple years.

#### Tasks
- **Leftover Method**: Discretionary = leftover after mandatory items.
- **Rule-Based**: A configuration that says “take last year’s discretionary and multiply by 1.05 (5% growth).”
- **Allow Switching**: Let the scenario config specify which method applies each year or overall.

#### Potential Pitfalls / Misconceptions
A new user might assume the system automatically optimizes discretionary across the entire timeline. At this stage, it’s per-year logic only.

#### Success Criteria
We can run the exact same scenario but produce different annual results depending on the chosen discretionary method. The user understands that at this point, we do not yet handle multi-year smoothing or constraints.

### 4.4 Phase 4: Multi-Year Optimization for Discretionary (If Needed)

#### Purpose
Optionally implement a solver approach where discretionary across all years is found by meeting certain constraints and possibly maximizing final net worth or another objective.

#### Tasks
- **Define Variables**: \(D_1, D_2, \ldots, D_T\).
- **Constraints**: e.g., \(\Delta D_t \leq 7\%\), final retirement >= $X, or other user-defined rules.
- **Objective (Example)**: Maximize final net worth or total discretionary.
- Use a Math Solver in Python or a chosen environment.

#### Potential Pitfalls / Misconceptions
If a user sees “optimization,” they might assume the tool automatically invests or picks best stocks. Clarify that this optimization is about discretionary spending and certain constraints, not micro-level investment choices.

#### Success Criteria
The solver yields a feasible path of discretionary for each year that meets constraints. The system gracefully reports if no solution is found (e.g., if constraints are contradictory).

### 4.5 Phase 5: Comprehensive Savings Integration (Retirement, College, Emergency)

#### Purpose
Combine all saving targets (e.g., 401k, Roth IRA, college funds) to see how they accumulate over time.

#### Tasks
- **Retirement Model**: Show pre-tax 401k, possible employer matching, or IRA contributions.
- **College Funds**: Possibly lumps or ongoing contributions.
- **Emergency Fund**: Keep a buffer that might be 3–6 months of living expenses.
- Adjust leftover or discretionary accordingly after these saving allocations.

#### Potential Pitfalls / Misconceptions
A casual reader might confuse “emergency fund” with leftover discretionary. Emphasize that an emergency fund is typically a separate bucket not spent on day-to-day items.

#### Success Criteria
Each year’s ledger includes updated balances for these accounts. The system ensures mandatory savings or required contributions are allocated before finalizing discretionary.

### 4.6 Phase 6: Detailed Taxes and Inflation

#### Purpose
Move from a flat tax to a more realistic bracket system. Incorporate inflation to see real vs. nominal values.

#### Tasks
- **TaxModel**: Expand logic to handle multiple brackets or regional complexities.
- **Inflation**: Year over year, costs or incomes rise by a certain percentage (from scenario config).
- **Real vs. Nominal**: Optionally track amounts in “today’s dollars.”

#### Potential Pitfalls / Misconceptions
Some might think it covers every detail of US tax law or international laws. Clarify that it’s an extensible system. Users add or modify rules as needed.

#### Success Criteria
Over a 20-year run, living expenses, taxes, and incomes reflect inflation, and the final results can be displayed both nominally and in real purchasing power terms.

### 4.7 Phase 7: Probabilistic / Stochastic Elements (If Desired)

#### Purpose
Model uncertainties like job-loss risk, varying investment returns, or windfalls.

#### Tasks
- **Random Draws**: Each year, sample events or returns from a distribution.
- **Monte Carlo**: Repeat the entire simulation many times to produce percentile outcomes.

#### Potential Pitfalls / Misconceptions
Readers might assume the system is automatically connected to real market data. Clarify it’s based on user-provided distributions or assumptions (e.g., “stock returns ~ Normal(µ=5%, σ=10%)”).

#### Success Criteria
We can see best/worst-case scenarios, average outcomes, etc. Helps evaluate risk tolerance and how robust the plan is to unexpected changes.

### 4.8 Phase 8: Additional Refinements

#### Purpose
Address more specialized or advanced features once the core system is stable.

#### Tasks
- **Real Estate Nuances**: Selling/buying multiple properties, variable property tax rates.
- **Partial Retirement**: Gradual reduction in income or partial Social Security.
- **Estate Planning**: Inheritance rules, advanced wealth transfer.

#### Potential Pitfalls / Misconceptions
A naive user might think these come “out of the box” from day one. Emphasize it’s an extension step, not core.

#### Success Criteria
The system can handle the complexities of advanced real-life scenarios for those who need them, without cluttering the baseline structure.