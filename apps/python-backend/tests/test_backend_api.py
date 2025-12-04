import pytest
from fastapi.testclient import TestClient

from financial_planner.backend_api import app

client = TestClient(app)

SCENARIO_YAML = """
start_year: 2024
end_year: 2024
inflation_rate: 0.0
household:
  living_costs: 1000
  housing_costs: 1000
  members:
    - name: A
      income: 5000
      tax_rate: 0.2
"""


def test_get_results_without_run():
    response = client.get("/get-results")
    assert response.status_code == 404


def test_full_simulation_flow():
    files = {"file": ("scenario.yaml", SCENARIO_YAML, "application/x-yaml")}
    upload_resp = client.post("/upload-scenario", files=files)
    assert upload_resp.status_code == 200

    run_resp = client.post("/run-simulation")
    assert run_resp.status_code == 200

    results_resp = client.get("/get-results")
    assert results_resp.status_code == 200
    data = results_resp.json()
    assert "results" in data
    assert data["results"]
