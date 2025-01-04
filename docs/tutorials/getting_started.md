# Getting Started

Welcome to the Getting Started tutorial. In this guide, you’ll install the project’s dependencies, set up your environment, and run your very first simulation.

## 1. Prerequisites

- Python 3.8+ installed on your system.
- Basic familiarity with the command line.
- (Recommended) A virtual environment tool like venv or conda to keep dependencies isolated.

## 2. Clone or Download the Project

### Clone via Git

```bash
git clone https://github.com/your-username/financial-planner.git
cd financial-planner
```

### Or Download a Zip

- Download the latest release.
- Extract the zip and `cd` into the folder.

## 3. Install Dependencies

Inside the project folder:

```bash
# Using a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # or on Windows: .venv\Scripts\activate

# Then install required packages
pip install -r requirements.txt
```

## 4. Basic Project Structure

Here’s a simplified look at what’s inside:

```bash
financial-planner/
├── src/
├──── financial_planner/
│     ├── simulation_engine.py
│     ├── household.py
│     ├── person.py
│     └── ...
├── docs/
│   ├── tutorials/
│   ├── how_to/
│   ├── explanation/
│   └── reference/  # Auto-generated API docs
├── scripts/
│   ├── lint.py
│   └── ...
├── tests/
│   └── ...
├── pyproject.toml
├── requirements.txt
└── scenario.yaml
```

- `financial_planner/`: Core logic for simulations, taxes, etc.
- `docs/`: Project documentation (what you’re reading now!).
- `scripts/`: Utility scripts like linters.
- `tests/`: Automated tests ensuring the system’s correctness.
- `pyproject.toml`: Project configuration file.
- `scenario.yaml`: A sample scenario file.

## 5. Run Your First Command

Navigate to the project’s root directory (where `scenario.yaml` resides). Run a simple simulation via Python (replace with your actual script if needed):

```bash
python main.py
```

Or, if you have a dedicated CLI:

```bash
python -m financial_planner.cli --scenario scenario.yaml
```

You’ll see debug logs or results in your terminal.

## 6. Next Steps

- **Check the Output**: You might see a `financial_simulation_results.csv` file or console output with yearly breakdowns.
- **Explore**: Move on to the First Simulation to modify and interpret a custom scenario.
- **See Also**: How-To Guides for quick instructions on specific tasks.

Congratulations! You’ve set up your environment and run the system. If you ran into errors, head over to the How-To Guides or consult our Explanation for deeper context.