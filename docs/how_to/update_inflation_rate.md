# How to Update the Inflation Rate

**Goal:** Change the assumed inflation rate in your simulation to see how expenses evolve.

## 1. Open Your Scenario File
Locate your scenario configuration file (e.g., `my_scenario.yaml`) and open it in a text editor.

```yaml
start_year: 2024
end_year: 2028
inflation_rate: 0.02
household:
    ...
```

## 2. Modify `inflation_rate`
Change the `inflation_rate` to your desired value. For example, to set it to 3%:

```yaml
inflation_rate: 0.03
```

Or to set it to 1%:

```yaml
inflation_rate: 0.01
```

## 3. Re-run the Simulation
After saving your changes, execute the simulation again:

```bash
python main.py --scenario my_scenario.yaml
```

## 4. Interpret the Impact
- **Expenses Adjustment:** Both `living_costs` and `housing_costs` will be multiplied by (1 + `inflation_rate`) annually.
- **Higher Inflation:** Leads to higher expenses, potentially reducing leftover funds over time.
- **Lower Inflation:** Keeps expenses more stable, possibly increasing leftover funds.

## 5. Further Reading
- For a deeper understanding, see [Architecture Overview](#).
- Want to also adjust tax rates? Check [Adjust Tax Rate](#).
