# Design Choices

This page explains why we made certain architecture and financial decisions.

## 1. Scenario-Centric Approach

**Rationale**

- **Flexibility**: A YAML/JSON scenario file can capture many user-specific details without hardcoding them in the code.
- **Comparisons**: Users can easily swap or create multiple scenarios to test different what-if outcomes.

**Consequences**

- **Ease of Extension**: Adding new fields (e.g., advanced events) typically just requires updating config parsing and relevant simulation logic.
- **Clear Separation**: The core simulation logic is decoupled from user input specifics.

## 2. Household and Person Abstraction

**Rationale**

- **Realistic Modeling**: Many financial questions revolve around a group (family, partners, etc.), not just individuals.
- **Aggregation**: Summing incomes, taxes, and costs at the household level is straightforward.

**Consequences**

- **Scalability**: Adding more Person objects or shared expenses is consistent with everyday scenarios.
- **Simplicity**: Abstracting each member’s tax or income logic avoids duplication.

## 3. Yearly Iteration

**Rationale**

- **Long-Term Projection**: A year-by-year approach aligns with many real-world financial calculations (tax returns, yearly raises, annual expenses).
- **Incremental Complexity**: We can add monthly or quarterly details in the future if needed.

**Consequences**

- **Event Handling**: Time-based triggers (house purchases, job changes) can slot naturally into yearly loops.
- **Computational Efficiency**: A single pass over each year is generally performant for 10–30+ year scenarios.

## 4. Minimal Initial Tax Model

**Rationale**

- **Start Simple**: Flat rates or single-bracket models help validate the system’s architecture without heavy complexity.
- **User Configurable**: Encourage advanced users to extend or override the tax logic in code.

**Consequences**

- **Easier Testing**: A straightforward tax model means fewer variables in early test phases.
- **Roadmap**: Leaves room for advanced bracket-based tax expansions.

## 5. Balancing Stability vs. Change

**Rationale**

- **Evolving Project**: Some features may rapidly evolve. Documenting them prematurely can confuse or create maintenance burdens.
- **Focus on Core**: We’ve chosen to detail stable, core behaviors (like yearly iteration and base scenario structure) while keeping future expansions at a high level.

**Consequences**

- **Incremental Documentation**: As new features stabilize, we can flesh out new tutorials or how-to guides.

## 6. Conclusion

By thoughtfully structuring the system around scenarios, year-by-year simulations, and a clear distinction between Household and Person objects, we’ve built a flexible foundation that’s both easy to use and ready to expand. Future improvements will deepen financial modeling without breaking existing core designs.

For more details on how these components interact at runtime, see the [Architecture Overview](#) or check our [Reference docs](#).
