## First Simulation
Now that you’ve installed everything and confirmed the project runs, let’s create and run a simple scenario. This tutorial will walk you through editing a minimal configuration and understanding the results.

## 1. Copy the Example Scenario
You may have a file named `scenario.yaml`. Make a copy, like `my_scenario.yaml`, and open it in a text editor:

```yaml
start_year: 2024
end_year: 2026
inflation_rate: 0.02
household:
  living_costs: 50000
  housing_costs: 20000
  members:
    - name: "Jason"
      income: 80000
      tax_rate: 0.25
    - name: "Linda"
      income: 60000
      tax_rate: 0.20
```

## 2. Modify the File (Optional)
- Adjust Years: `start_year: 2023`.
- Tweak Incomes: Raise or lower each member’s income.
- Set Different Inflation: `inflation_rate: 0.01` for 1% instead of 2%.

## 3. Run the Simulation
Use whichever command you normally use. After it finishes, check your results CSV or logs:

```bash
python main.py --scenario my_scenario.yaml
```

## 4. Interpreting the Results
Check the generated CSV (for example, `financial_simulation_results.csv`) to see columns like:

- **Year**: Which simulation year (2024, 2025, ...).
- **Total Income**: Sum of all household members’ incomes that year (with any growth applied).
- **Total Taxes**: Combined taxes for the household.
- **Total Mandatory Expenses**: `living_costs + housing_costs`, adjusted by inflation (if applicable).
- **Leftover**: The difference after taxes and mandatory expenses.
- **Naive Discretionary**: Currently the same as leftover, unless you’ve added advanced features.

## 5. Next Steps
- **Experiment**: Change the inflation rate or add another household member to see how it affects leftover amounts.
- **How-To Guides**: For quick tutorials on specific tasks (e.g., adjusting tax rates).
- **Explanations**: Learn why the system is designed this way in the Architecture Overview.

You’ve now seen how to run a basic simulation and interpret the CSV output. Well done!