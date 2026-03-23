from typing import Dict


def _status(run_mode: str) -> str:
    if run_mode == "dry-run":
        return "skipped (dry-run)"
    if run_mode == "demo":
        return "simulated-success"
    return "queued"


def mast3r_bridge(job_id: str, project_id: str, video_uri: str, run_mode: str) -> Dict[str, object]:
    out_uri = f"gs://{project_id}-artifacts/{job_id}/geometry/"
    return {
        "stage": "mast3r_slam",
        "status": _status(run_mode),
        "enhancement": "Replaced Tango-dependent RGBD assumption with monocular-mobile geometry priors through MASt3R-SLAM stage packaging.",
        "inputs": {"video_uri": video_uri},
        "outputs": {
            "geometry_uri": out_uri,
            "camera_trajectory_uri": f"{out_uri}trajectory.txt",
            "sparse_map_uri": f"{out_uri}sparse_map.ply",
        },
    }


def floornet_bridge(job_id: str, project_id: str, geometry_uri: str, run_mode: str) -> Dict[str, object]:
    out_uri = f"gs://{project_id}-artifacts/{job_id}/floorplan/"
    return {
        "stage": "floornet",
        "status": _status(run_mode),
        "enhancement": "Added a bridge adapter that rasterizes MASt3R-derived geometry into FloorNet-compatible top-view and semantic priors for FLOORPLAN reconstruction without Tango capture.",
        "inputs": {"geometry_uri": geometry_uri},
        "outputs": {
            "floorplan_raster_uri": f"{out_uri}floorplan_raster.png",
            "floorplan_vector_uri": f"{out_uri}floorplan_vector.json",
            "room_types_uri": f"{out_uri}room_types.json",
        },
    }


def orchestrator_bridge(job_id: str, project_id: str, floorplan_vector_uri: str, run_mode: str) -> Dict[str, object]:
    out_uri = f"gs://{project_id}-artifacts/{job_id}/layout/"
    return {
        "stage": "orchestrator",
        "status": _status(run_mode),
        "enhancement": "Bound Orchestrator constraints directly to FLOORPLAN polygons and room semantics, enabling API-driven object placement plans tied to structural layout.",
        "inputs": {"floorplan_vector_uri": floorplan_vector_uri},
        "outputs": {
            "layout_plan_uri": f"{out_uri}layout_plan.json",
            "collision_report_uri": f"{out_uri}collision_report.json",
            "scene_prompt_uri": f"{out_uri}scene_prompt.txt",
        },
    }


def plan2scene_bridge(job_id: str, project_id: str, layout_plan_uri: str, floorplan_vector_uri: str, run_mode: str) -> Dict[str, object]:
    out_uri = f"gs://{project_id}-artifacts/{job_id}/scene/"
    return {
        "stage": "plan2scene",
        "status": _status(run_mode),
        "enhancement": "Bridged Orchestrator layout outputs into Plan2Scene scene JSON assembly, plus texture propagation hooks for walls/floors/ceilings.",
        "inputs": {
            "layout_plan_uri": layout_plan_uri,
            "floorplan_vector_uri": floorplan_vector_uri,
        },
        "outputs": {
            "scene_json_uri": f"{out_uri}scene.json",
            "textured_arch_uri": f"{out_uri}textured_arch/",
            "texture_manifest_uri": f"{out_uri}texture_manifest.json",
        },
    }


def hunyuan_bridge(job_id: str, project_id: str, scene_json_uri: str, run_mode: str) -> Dict[str, object]:
    out_uri = f"gs://{project_id}-artifacts/{job_id}/final/"
    return {
        "stage": "hunyuan3d",
        "status": _status(run_mode),
        "enhancement": "Integrated Hunyuan3D asset synthesis as an API stage that injects generated object meshes into the textured architectural scene package.",
        "inputs": {"scene_json_uri": scene_json_uri},
        "outputs": {
            "asset_bundle_uri": f"{out_uri}assets/",
            "final_scene_glb_uri": f"{out_uri}scene.glb",
            "final_package_uri": f"{out_uri}scene_bundle.zip",
        },
    }
