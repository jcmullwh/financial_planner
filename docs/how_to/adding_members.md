# How to Add Household Members

**Goal:** Include additional family members or earners in the simulation.

## Steps

### 1. Open the Scenario File
Locate your scenario configuration file (e.g., `my_scenario.yaml`) and open it in a text editor.

```yaml
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

### 2. Add a New Entry
Add a new Person entry to the members list. For example, to add Alex:

```yaml
- name: "Alex"
    income: 40000
    tax_rate: 0.18
```

Your updated members section will look like this:

```yaml
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
        - name: "Alex"
            income: 40000
            tax_rate: 0.18
```

### 3. Run and Verify
Execute the simulation with the updated scenario:

```bash
python main.py --scenario my_scenario.yaml
```

Check the output CSV or logs to ensure that Alex’s income and taxes are now included in the household totals.

### 4. Next Steps
- **Further Customization:** Adjust Alex’s income or tax_rate as needed.
- **Add More Members:** Repeat the process to include additional household members.
- **Combine with Other Adjustments:** Modify inflation rates or other financial parameters to see combined effects.

For more detailed information on financial modeling or system architecture, refer to the Explanation section or consult the Reference docs.
