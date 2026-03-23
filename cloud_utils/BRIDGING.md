# BRIDGING LAYER: MODULE-TO-MODULE API FLOW

This document defines how `fyp-2026` bridges independent research modules into one API-style orchestration chain.

## Contribution Layer Summary

## 1) `MASt3R-SLAM` Enhancement
- Original gap: legacy floorplan pipelines (e.g., Tango-era assumptions) expect depth-heavy input constraints.
- Our bridge contribution: package monocular mobile video into geometry and trajectory artifacts reusable by downstream stages.
- Output contract:
  - `geometry_uri`
  - `camera_trajectory_uri`
  - `sparse_map_uri`

## 2) `FloorNet` Enhancement
- Original gap: FloorNet is not natively wired to MASt3R-SLAM outputs.
- Our bridge contribution: transform MASt3R geometry into FloorNet-compatible top-view priors and room-semantic envelopes.
- Output contract:
  - `floorplan_raster_uri`
  - `floorplan_vector_uri`
  - `room_types_uri`

## 3) `Orchestrator` Enhancement
- Original gap: object layout planning is usually prompt-only and disconnected from structural priors.
- Our bridge contribution: bind ORCHESTRATOR prompts and constraints directly to FLOORPLAN geometry and room labels.
- Output contract:
  - `layout_plan_uri`
  - `collision_report_uri`
  - `scene_prompt_uri`

## 4) `Plan2Scene` Enhancement
- Original gap: scene texturing pipelines typically require manual staging between layout and texture generation.
- Our bridge contribution: convert ORCHESTRATOR layout plan + FLOORPLAN vectors into a single texture-ready scene package.
- Output contract:
  - `scene_json_uri`
  - `textured_arch_uri`
  - `texture_manifest_uri`

## 5) `Hunyuan3D-2` Enhancement
- Original gap: generated assets are not automatically inserted into full architectural pipelines.
- Our bridge contribution: inject API-generated assets into the final scene package as deployable artifacts.
- Output contract:
  - `asset_bundle_uri`
  - `final_scene_glb_uri`
  - `final_package_uri`

## End-to-End API Graph

```text
POST /pipeline/run
  -> mast3r_slam bridge
  -> floornet bridge
  -> orchestrator bridge
  -> plan2scene bridge
  -> hunyuan3d bridge
  -> scene bundle
```

## Runtime Modes
- `dry-run`: no execution, contract-only status
- `demo`: simulated success for all enabled stages
- `full`: queue-style status for production scheduler integration
