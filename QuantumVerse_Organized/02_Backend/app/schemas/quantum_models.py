from typing import List, Optional

from pydantic import BaseModel, Field

class ProbabilityCrossSection(BaseModel):
    x: List[float]
    z: List[float]
    density: List[float] 

class AtomicSimulationRequest(BaseModel):
    n: int = Field(1, ge=1, le=6)
    l: int = Field(0, ge=0, le=5)
    m: int = Field(0, ge=-5, le=5)

    grid_size: int = Field(35, ge=15, le=60)
    extent: float = Field(12.0, gt=0, le=30)
    threshold: float = Field(0.03, gt=0, lt=1)


class ProbabilityCloud(BaseModel):
    x: List[float]
    y: List[float]
    z: List[float]
    density: List[float]


class AtomicSimulationResponse(BaseModel):
    cross_section: ProbabilityCrossSection
    success: bool
    atom: str
    n: int
    l: int
    m: int
    orbital: str
    energy_ev: float
    bohr_radius_m: float
    point_count: int
    probability_cloud: ProbabilityCloud
    error: Optional[str] = None
