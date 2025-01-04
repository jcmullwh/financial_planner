# How to Adjust Tax Rates

**Goal:** Change an individual’s tax rate to reflect different tax scenarios.

## 1. Edit the Scenario

Open your scenario configuration file (e.g., `my_scenario.yaml`) and locate the members section:

```yaml
household:
    members:
        - name: "Jason"
            income: 80000
            tax_rate: 0.25
        - name: "Linda"
            income: 60000
            tax_rate: 0.20
```

## 2. Change the Value

Modify the `tax_rate` for the desired household member. For example, to increase Linda’s tax rate to 30%:

```yaml
- name: "Linda"
    income: 60000
    tax_rate: 0.30
```

## 3. Run the Simulation

After saving your changes, execute the simulation:

```bash
python main.py --scenario my_scenario.yaml
```

## 4. Check the Output

- **Leftover Funds:** Increasing the tax rate will likely decrease the leftover amount.
- **Comparison:** Compare the new results with previous runs to observe the impact of the tax rate change.

## 5. Further Guidance

- **Multiple Adjustments:** Feel free to adjust tax rates for multiple members to simulate more complex scenarios.
- **Combine with Inflation Changes:** To see compounded effects, consider also modifying the inflation rate using `Update Inflation Rate`.
- **Advanced Tax Logic:** For more detailed tax configurations, refer to the Reference docs or the Explanation.
