from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.user import User
from app.quantum.models.hydrogen import (
    describe_state,
    generate_cross_section,
    generate_probability_cloud,
    validate_quantum_numbers,
)

from app.schemas.quantum_models import (
    AtomicSimulationRequest,
    AtomicSimulationResponse,
    ProbabilityCloud,
    ProbabilityCrossSection,
)

router = APIRouter(
    prefix="/quantum-models",
    tags=["quantum-models"],
)


@router.post(
    "/atomic/simulate",
    response_model=AtomicSimulationResponse,
)
async def simulate_atomic_model(
    body: AtomicSimulationRequest,
    user: User = Depends(get_current_user),
):
    try:
        validate_quantum_numbers(body.n, body.l, body.m)

        state = describe_state(
            body.n,
            body.l,
            body.m,
        )

        cloud = generate_probability_cloud(
            n=body.n,
            l=body.l,
            m=body.m,
            grid_size=body.grid_size,
            extent=body.extent,
            threshold=body.threshold,
        )

        cross_section = generate_cross_section(
            n=body.n,
            l=body.l,
            m=body.m,
            grid_size=80,
            extent=body.extent,
        )

        return AtomicSimulationResponse(
            success=True,
            atom="Hydrogen",
            n=body.n,
            l=body.l,
            m=body.m,
            orbital=state["orbital"],
            energy_ev=state["energy_ev"],
            bohr_radius_m=state["bohr_radius_m"],
            point_count=len(cloud["x"]),
            probability_cloud=ProbabilityCloud(**cloud),
            cross_section=ProbabilityCrossSection(**cross_section),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
