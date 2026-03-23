from typing import Dict, List

from pydantic import BaseModel, Field


class ArtifactEnvelope(BaseModel):
    uri: str
    format: str
    produced_by: str


class StageExecution(BaseModel):
    stage: str
    status: str
    enhancement: str
    inputs: Dict[str, str] = Field(default_factory=dict)
    outputs: Dict[str, str] = Field(default_factory=dict)


class BridgeTrace(BaseModel):
    job_id: str
    stages: List[StageExecution]
