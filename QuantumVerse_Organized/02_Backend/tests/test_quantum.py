"""Tests for the Qiskit quantum engine."""
import pytest
from app.quantum.simulator import run_simulation
from app.quantum.step_executor import execute_step
from app.quantum.algorithms.grover import run_grover
from app.quantum.algorithms.deutsch_jozsa import run_deutsch_jozsa
from app.quantum.algorithms.qft import run_qft
from app.quantum.algorithms.teleportation import run_teleportation


def test_single_qubit_x_gate():
    ops = [{"gate": "X", "targets": [0], "controls": [], "column": 0}]
    result = run_simulation(1, 1, ops, shots=512)
    assert result["success"]
    assert result["counts"].get("1", 0) > 490, "X gate should flip |0> to |1>"


def test_hadamard_superposition():
    ops = [{"gate": "H", "targets": [0], "controls": [], "column": 0}]
    result = run_simulation(1, 1, ops, shots=1000)
    assert result["success"]
    counts = result["counts"]
    assert abs(counts.get("0", 0) - counts.get("1", 0)) < 150, "H gate should give ~50/50"


def test_bell_state():
    ops = [
        {"gate": "H",    "targets": [0], "controls": [],  "column": 0},
        {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
    ]
    result = run_simulation(2, 2, ops, shots=1000)
    assert result["success"]
    counts = result["counts"]
    # Bell state |00> + |11> - only 00 and 11 should appear
    assert counts.get("01", 0) < 50
    assert counts.get("10", 0) < 50


def test_step_executor():
    ops = [
        {"gate": "H", "targets": [0], "controls": [], "column": 0},
        {"gate": "X", "targets": [1], "controls": [], "column": 1},
    ]
    result = execute_step(2, ops, 0)
    assert result["success"]
    assert result["gate_applied"] == "H"
    assert "probabilities" in result


def test_grover():
    result = run_grover(3, 5)
    assert result["success"]
    assert result["target_probability"] > 0.5, "Grover should have high probability for target"


def test_deutsch_jozsa_constant():
    result = run_deutsch_jozsa("constant_zero", 3)
    assert result["success"]
    assert result["result"] == "constant"


def test_deutsch_jozsa_balanced():
    result = run_deutsch_jozsa("balanced", 3)
    assert result["success"]
    assert result["result"] == "balanced"


def test_qft():
    result = run_qft(3, 0)
    assert result["success"]
    assert "probabilities" in result


def test_teleportation():
    result = run_teleportation("plus")
    assert result["success"]
    assert "steps" in result
    assert len(result["steps"]) == 5
