"""Circuit export / import endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.models.user import User
from app.quantum.engine import build_circuit

router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    qubits: int
    classical_bits: int
    operations: list[dict[str, Any]]
    format: str = "qasm"  # qasm | python | json


@router.post("/circuit")
async def export_circuit(body: ExportRequest, user: User = Depends(get_current_user)):
    qc = build_circuit(body.qubits, body.classical_bits, body.operations)

    if body.format == "qasm":
        code = qc.qasm() if hasattr(qc, "qasm") else "# QASM export requires Qiskit 0.x"
        return PlainTextResponse(code, media_type="text/plain")

    elif body.format == "python":
        ops = body.operations
        lines = [
            "from qiskit import QuantumCircuit",
            "from qiskit_aer import AerSimulator",
            "",
            f"qc = QuantumCircuit({body.qubits}, {body.classical_bits})",
        ]
        for op in ops:
            gate = op.get("gate", "").lower()
            targets = op.get("targets", [])
            controls = op.get("controls", [])
            if gate in ("h", "x", "y", "z", "s", "t", "sdg", "tdg") and targets:
                lines.append(f"qc.{gate}({targets[0]})")
            elif gate in ("cnot", "cx") and targets and controls:
                lines.append(f"qc.cx({controls[0]}, {targets[0]})")
            elif gate == "cz" and targets and controls:
                lines.append(f"qc.cz({controls[0]}, {targets[0]})")
            elif gate == "swap" and len(targets) >= 2:
                lines.append(f"qc.swap({targets[0]}, {targets[1]})")
            elif gate == "measure" and targets:
                lines.append(f"qc.measure({targets[0]}, {targets[0]})")
        lines += [
            "",
            "sim    = AerSimulator()",
            "result = sim.run(qc, shots=1024).result()",
            "counts = result.get_counts()",
            "print(counts)",
        ]
        return PlainTextResponse("\n".join(lines), media_type="text/plain")

    elif body.format == "json":
        import json
        return PlainTextResponse(
            json.dumps({"qubits": body.qubits, "classical_bits": body.classical_bits, "operations": body.operations}, indent=2),
            media_type="application/json",
        )

    raise HTTPException(400, "Format must be qasm, python, or json")
