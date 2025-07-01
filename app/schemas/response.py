from typing import List, Optional
from pydantic import BaseModel


class SolvedRouteStep(BaseModel):
    type: str  # "start", "pickup", "delivery", "end"
    id: Optional[int] = None  # shipment_step id
    location: Optional[List[float]] = None  # lon, lat
    arrival_time: Optional[str] = None
    finish_time: Optional[str] = None


class SolvedRoute(BaseModel):
    vehicle_id: int
    steps: List[SolvedRouteStep]
    total_distance_meters: Optional[float] = None
    total_duration_seconds: Optional[float] = None


class OptimizationSolution(BaseModel):
    routes: List[SolvedRoute]
    unassigned_shipments: List[int] = []


class TaskResult(BaseModel):
    task_id: str
    status: str  # "PENDING", "STARTED", "SUCCESS", "FAILURE"
    solution: Optional[OptimizationSolution] = None
    error: Optional[str] = None
