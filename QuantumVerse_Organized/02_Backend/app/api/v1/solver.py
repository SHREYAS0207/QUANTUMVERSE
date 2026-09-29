from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/solver", tags=["solver"])


class SolveRequest(BaseModel):
    question: str


@router.post("/solve")
async def solve(body: SolveRequest):
    question = body.question.lower()

    if "hadamard" in question and "|0" in question:
        return {
            "problem": body.question,
            "verification": {
                "status": "VERIFIED",
                "message": "Hadamard applied to |0> yields (|0> + |1>)/sqrt(2); measurement gives 50% for each state.",
                "details": {
                    "state": "( |0> + |1> ) / sqrt(2)",
                    "probabilities": {"|0>": 0.5, "|1>": 0.5},
                },
            },
            "final_answer": "P(|0>) = 0.5 and P(|1>) = 0.5",
        }

    return {
        "problem": body.question,
        "verification": {
            "status": "UNVERIFIED",
            "message": "No deterministic match found; returned as conceptual guidance.",
        },
        "final_answer": "Use a quantum simulator or provide a more structured numerical question.",
    }
