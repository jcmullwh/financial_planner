# tests/test_report_generator.py

import os
import tempfile
from decimal import Decimal

import pytest

from financial_planner.report_generator import generate_report


def test_generate_report_success():
    results = [
        {
            "year": Decimal("2024"),
            "total_income": Decimal("140000.00"),
            "total_taxes": Decimal("35000.00"),
            "total_mandatory_expenses": Decimal("70000.00"),
            "leftover": Decimal("35000.00"),
            "naive_discretionary": Decimal("35000.00"),
        },
        {
            "year": Decimal("2025"),
            "total_income": Decimal("144200.00"),
            "total_taxes": Decimal("32960.00"),
            "total_mandatory_expenses": Decimal("71400.00"),
            "leftover": Decimal("39740.00"),
            "naive_discretionary": Decimal("39740.00"),
        },
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as tmp:
        tmp_path = tmp.name

    try:
        generate_report(results, filename=tmp_path)
        assert os.path.exists(tmp_path)

        with open(tmp_path) as f:
            content = f.read()
            assert "Year,Total Income,Total Taxes,Total Mandatory Expenses,Leftover,Naive Discretionary" in content
            assert "2024,140000.00,35000.00,70000.00,35000.00,35000.00" in content
            assert "2025,144200.00,32960.00,71400.00,39740.00,39740.00" in content
    finally:
        os.remove(tmp_path)


def test_generate_report_no_results():
    results = []
    with pytest.raises(RuntimeError, match="No simulation results to report."):
        generate_report(results)


def test_generate_report_file_write_error():
    results = [
        {
            "year": Decimal("2024"),
            "total_income": Decimal("140000.00"),
            "total_taxes": Decimal("35000.00"),
            "total_mandatory_expenses": Decimal("70000.00"),
            "leftover": Decimal("35000.00"),
            "naive_discretionary": Decimal("35000.00"),
        }
    ]

    # Attempt to write to a directory (which should fail)
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(RuntimeError):
            # Directories cannot be opened as files, should raise an IOError
            generate_report(results, filename=tmp_dir)
