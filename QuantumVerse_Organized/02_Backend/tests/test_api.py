"""Integration tests for QuantumVerse API."""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_signup_and_login():
    email = f"test_{uuid.uuid4().hex[:10]}@quantumverse.ai"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Signup
        res = await client.post("/api/v1/auth/signup", json={
            "name": "Test User", "email": email,
            "password": "testpass123", "learning_level": "beginner",
        })
        assert res.status_code == 201
        token = res.json()["access_token"]

        # Login should work with the created account
        login_res = await client.post("/api/v1/auth/login", json={
            "email": email,
            "password": "testpass123",
        })
        assert login_res.status_code == 200
        assert login_res.json()["email"] == email

        # Profile
        profile = await client.get("/api/v1/auth/profile", headers={"Authorization": f"Bearer {token}"})
        assert profile.status_code == 200
        assert profile.json()["name"] == "Test User"


@pytest.mark.anyio
async def test_algorithms_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/algorithms")
    assert res.status_code == 200
    assert len(res.json()["algorithms"]) == 4


@pytest.mark.anyio
async def test_admin_stats_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/admin/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["users"] >= 0
    assert data["circuits"] >= 0


@pytest.mark.anyio
async def test_challenges_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/challenges")
    assert res.status_code == 200
    data = res.json()
    assert len(data["challenges"]) >= 1


@pytest.mark.anyio
async def test_solver_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/v1/solver/solve", json={
            "question": "Apply the Hadamard gate to |0> and explain the measurement probabilities."
        })
    assert res.status_code == 200
    data = res.json()
    assert data["verification"]["status"] in {"VERIFIED", "UNVERIFIED"}
