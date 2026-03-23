# Cloud Utils (Cloud Run Orchestrator Scaffold)

This folder provides a realistic serverless scaffold for presenting `fyp-2026` as a unified Cloud Run deployment.

## What this includes

- `main.py`: FastAPI orchestrator endpoint (`/pipeline/run`) with staged module flow + bridge trace
- `bridges.py`: stage-level adapters describing per-module handoff behavior
- `contracts.py`: shared response contract models for bridge artifacts
- `BRIDGING.md`: module-by-module contribution and bridging notes
- `requirements.txt`: minimal web runtime dependencies
- `Dockerfile`: container image definition for Cloud Run
- `cloudrun-service.yaml`: Knative Service manifest for Cloud Run deployment

## Pipeline shape

The orchestrator represents this stage chain:

1. `mast3r_slam` → geometry and camera priors
2. `floornet` → FLOORPLAN extraction
3. `orchestrator` → semantic object layout planning
4. `plan2scene` → architectural texturing and propagation
5. `hunyuan3d` → asset generation and final packaging

## API response extras

`POST /pipeline/run` returns:
- `stages`: status map for enabled modules
- `outputs`: final artifact URIs
- `bridge_trace`: stage-by-stage inputs/outputs/enhancement descriptions
- `contribution_layer`: concise summary of what the FYP integration adds per module

## Local run

```bash
cd /Users/vk/Downloads/fyp-2026
python -m venv .venv-cloud
source .venv-cloud/bin/activate
pip install -r cloud_utils/requirements.txt
uvicorn cloud_utils.main:app --host 0.0.0.0 --port 8080
```

## Example request

```bash
curl -X POST "http://localhost:8080/pipeline/run" \
  -H "Content-Type: application/json" \
  -d '{
    "video_uri": "gs://demo-inputs/sample-room.mp4",
    "project_id": "fyp-2026",
    "run_mode": "demo"
  }'
```

## Cloud Run deployment (reference)

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/fyp-2026/fyp-2026-orchestrator:latest .
gcloud run services replace cloud_utils/cloudrun-service.yaml --region REGION
```

> Note: this scaffold is intentionally integration-focused. Production deployment would add IAM, secrets management, queueing, artifact validation, and GPU strategy per stage.
