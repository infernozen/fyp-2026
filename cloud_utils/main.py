import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from cloud_utils.bridges import (
    floornet_bridge,
    hunyuan_bridge,
    mast3r_bridge,
    orchestrator_bridge,
    plan2scene_bridge,
)


class PipelineRequest(BaseModel):
    video_uri: str = Field(..., description="Input video URI (e.g., gs://bucket/path.mp4)")
    project_id: str = Field(default="fyp-2026", description="Logical project identifier")
    run_mode: str = Field(default="demo", description="demo | dry-run | full")
    enable_modules: List[str] = Field(
        default_factory=lambda: [
            "mast3r_slam",
            "floornet",
            "orchestrator",
            "plan2scene",
            "hunyuan3d",
        ]
    )


class PipelineResponse(BaseModel):
    job_id: str
    status: str
    started_at: str
    cloud_run_service: str
    region: str
    stages: Dict[str, str]
    outputs: Dict[str, str]
    bridge_trace: List[Dict[str, object]]
    contribution_layer: Dict[str, str]


app = FastAPI(title="FYP-2026 Cloud Orchestrator", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "service": os.getenv("K_SERVICE", "fyp-2026-orchestrator"),
        "region": os.getenv("REGION", "asia-south1"),
    }


@app.post("/pipeline/run", response_model=PipelineResponse)
def run_pipeline(payload: PipelineRequest) -> PipelineResponse:
    job_id = f"job-{uuid.uuid4().hex[:10]}"
    started_at = datetime.now(timezone.utc).isoformat()

    bridge_trace: List[Dict[str, object]] = []
    stage_status: Dict[str, str] = {}

    mast3r = mast3r_bridge(job_id, payload.project_id, payload.video_uri, payload.run_mode)
    if "mast3r_slam" in payload.enable_modules:
        bridge_trace.append(mast3r)
        stage_status["mast3r_slam"] = mast3r["status"]
    else:
        stage_status["mast3r_slam"] = "disabled"

    floornet = floornet_bridge(
        job_id,
        payload.project_id,
        mast3r["outputs"]["geometry_uri"],
        payload.run_mode,
    )
    if "floornet" in payload.enable_modules:
        bridge_trace.append(floornet)
        stage_status["floornet"] = floornet["status"]
    else:
        stage_status["floornet"] = "disabled"

    orchestrator = orchestrator_bridge(
        job_id,
        payload.project_id,
        floornet["outputs"]["floorplan_vector_uri"],
        payload.run_mode,
    )
    if "orchestrator" in payload.enable_modules:
        bridge_trace.append(orchestrator)
        stage_status["orchestrator"] = orchestrator["status"]
    else:
        stage_status["orchestrator"] = "disabled"

    plan2scene = plan2scene_bridge(
        job_id,
        payload.project_id,
        orchestrator["outputs"]["layout_plan_uri"],
        floornet["outputs"]["floorplan_vector_uri"],
        payload.run_mode,
    )
    if "plan2scene" in payload.enable_modules:
        bridge_trace.append(plan2scene)
        stage_status["plan2scene"] = plan2scene["status"]
    else:
        stage_status["plan2scene"] = "disabled"

    hunyuan = hunyuan_bridge(
        job_id,
        payload.project_id,
        plan2scene["outputs"]["scene_json_uri"],
        payload.run_mode,
    )
    if "hunyuan3d" in payload.enable_modules:
        bridge_trace.append(hunyuan)
        stage_status["hunyuan3d"] = hunyuan["status"]
    else:
        stage_status["hunyuan3d"] = "disabled"

    outputs = {
        "geometry_uri": mast3r["outputs"]["geometry_uri"],
        "floorplan_uri": floornet["outputs"]["floorplan_vector_uri"],
        "scene_json_uri": plan2scene["outputs"]["scene_json_uri"],
        "assets_uri": hunyuan["outputs"]["asset_bundle_uri"],
        "final_package_uri": hunyuan["outputs"]["final_package_uri"],
    }

    contribution_layer = {
        "mast3r_slam": "Monocular-mobile geometry packaging replaces Tango-bound capture assumptions.",
        "floornet": "Geometry-to-FLOORPLAN adapter injects FloorNet-compatible priors from MASt3R outputs.",
        "orchestrator": "Constraint-linked ORCHESTRATOR plans tied to FLOORPLAN topology and room semantics.",
        "plan2scene": "Scene JSON and texture propagation are auto-constructed from ORCHESTRATOR + FLOORPLAN outputs.",
        "hunyuan3d": "Asset generation stage API-injects synthesized meshes into final scene package.",
    }

    return PipelineResponse(
        job_id=job_id,
        status="accepted",
        started_at=started_at,
        cloud_run_service=os.getenv("K_SERVICE", "fyp-2026-orchestrator"),
        region=os.getenv("REGION", "asia-south1"),
        stages=stage_status,
        outputs=outputs,
        bridge_trace=bridge_trace,
        contribution_layer=contribution_layer,
    )
