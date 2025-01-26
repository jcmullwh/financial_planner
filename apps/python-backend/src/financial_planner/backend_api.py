
import yaml
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from financial_planner.report_generator import generate_report
from financial_planner.simulation_engine import SimulationEngine

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulation = SimulationEngine()
results = []


@app.post("/upload-scenario")
async def upload_scenario(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    print(f"Content-Type: {file.content_type}")  # Log the MIME type

    allowed_mime_types = [
        "application/x-yaml",
        "text/yaml",
        "text/plain",
        "application/yaml",
        "application/octet-stream",  # Added to accept 'application/octet-stream'
    ]

    if file.content_type not in allowed_mime_types:
        print("Warning: Unusual MIME type received.")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a YAML file.")

    try:
        content = await file.read()
        config = yaml.safe_load(content)
        if not isinstance(config, dict):
            raise ValueError("YAML content must be a dictionary at the top level.")
        simulation.store_config(config)
        print("[DEBUG] Scenario loaded successfully.")
        return {"message": "Scenario loaded successfully."}
    except yaml.YAMLError as e:
        print(f"[ERROR] YAML parsing error: {e}")
        raise HTTPException(status_code=400, detail=f"YAML parsing error: {e}")
    except Exception as e:
        print(f"[ERROR] {e!s}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/run-simulation")
def run_simulation():
    try:
        simulation.load_scenario(simulation.config)
        simulation.run_simulation()
        global results
        results = simulation.results
        # Optionally generate a report
        generate_report(results)
        return {"message": "Simulation run successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-results")
def get_results():
    if not results:
        raise HTTPException(status_code=404, detail="No simulation results found.")
    return {"results": results}
