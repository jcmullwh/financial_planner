# financial_planner/report_generator.py

import csv
from decimal import Decimal


def generate_report(results: list[dict[str, Decimal]], filename: str = "financial_simulation_results.csv") -> None:
    """
    Compiles and formats the simulation results into a readable CSV file with raw numerical values.

    Args:
        results (list[dict[str, Decimal]]): The list of yearly financial summaries.
        filename (str, optional): The name of the CSV file to save the results.
            Defaults to "financial_simulation_results.csv".
    """
    if not results:
        message = "No simulation results to report. Please run the simulation first."
        raise RuntimeError(message)

    headers = ["Year", "Total Income", "Total Taxes", "Total Mandatory Expenses", "Leftover", "Naive Discretionary"]

    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for result in results:
                writer.writerow(
                    {
                        "Year": int(result["year"]),
                        "Total Income": f"{result['total_income']:.2f}",
                        "Total Taxes": f"{result['total_taxes']:.2f}",
                        "Total Mandatory Expenses": f"{result['total_mandatory_expenses']:.2f}",
                        "Leftover": f"{result['leftover']:.2f}",
                        "Naive Discretionary": f"{result['naive_discretionary']:.2f}",
                    }
                )
        print(f"[INFO] Report generated and saved to {filename}")
    except OSError as e:
        error_message = "Failed to generate report."
        print(f"[ERROR] Failed to write report to {filename}: {e}")
        raise RuntimeError(error_message) from e
