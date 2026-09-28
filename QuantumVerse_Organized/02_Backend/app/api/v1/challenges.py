from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/challenges", tags=["challenges"])


CHALLENGES = [
    {
        "id": 1,
        "title": "Bell State Challenge",
        "description": "Build a 2-qubit circuit that creates a Bell state.",
        "topic": "entanglement",
        "difficulty": "easy",
        "xp_reward": 100,
    },
    {
        "id": 2,
        "title": "Superposition Challenge",
        "description": "Create a circuit that produces an equal superposition across two basis states.",
        "topic": "superposition",
        "difficulty": "medium",
        "xp_reward": 150,
    },
]


@router.get("")
async def list_challenges():
    return {"challenges": CHALLENGES}


@router.get("/{challenge_id}")
async def get_challenge(challenge_id: int):
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge
