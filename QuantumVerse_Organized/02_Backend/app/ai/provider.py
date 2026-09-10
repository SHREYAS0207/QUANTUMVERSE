"""LLM abstraction layer using OpenRouter."""
import httpx
from app.core.config import settings


SYSTEM_PROMPTS = {
    "beginner": """You are QubitAI, an expert quantum computing tutor for beginners.
Explain concepts using simple analogies (coins, light switches, balls in boxes).
Avoid heavy math. Focus on intuition. Keep answers concise (3-5 sentences max unless asked for more).
If asked about quantum gates, use visual analogies.""",

    "intermediate": """You are QubitAI, a quantum computing tutor for intermediate learners.
You can use linear algebra, Dirac notation (|0⟩, |1⟩), and Bloch sphere descriptions.
Explain the math but keep it accessible. Connect theory to real circuit implementations.""",

    "advanced": """You are QubitAI, an expert quantum computing mentor for advanced students.
Use full mathematical formalism: density matrices, tensor products, unitary operators, Hamiltonians.
Discuss quantum complexity theory, error correction, and NISQ-era limitations when relevant.""",
}

FALLBACK_RESPONSES = {
    "beginner": "Quantum computing uses the weird rules of quantum physics — like superposition (being in two states at once) and entanglement (spooky action at a distance) — to perform certain calculations exponentially faster than classical computers.",
    "intermediate": "Quantum computing leverages quantum mechanical phenomena — superposition, entanglement, and interference — to encode and process information in qubits, enabling polynomial or exponential speedups for specific problem classes.",
    "advanced": "Quantum computing exploits the exponentially large Hilbert space of n-qubit systems and quantum mechanical operations (unitary evolution, projective measurement) to solve certain computational problems in BQP that are believed classically intractable.",
}


async def get_ai_response(
    message: str,
    history: list[dict],
    difficulty: str = "beginner",
    context: dict | None = None,
) -> str:
    if not settings.OPENROUTER_API_KEY or settings.OPENROUTER_API_KEY == "your-openrouter-key-here":
        return _fallback_response(message, difficulty)

    system = SYSTEM_PROMPTS.get(difficulty, SYSTEM_PROMPTS["beginner"])
    if context:
        system += f"\n\nCurrent context: {context}"

    messages = [{"role": "system", "content": system}]
    messages.extend(history[-8:])  # last 8 messages for context
    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://quantumverse.ai",
                    "X-Title": "QuantumVerse AI",
                },
                json={
                    "model": settings.AI_MODEL,
                    "messages": messages,
                    "max_tokens": 800,
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return _fallback_response(message, difficulty)


def _fallback_response(message: str, difficulty: str) -> str:
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["superposition", "what is quantum"]):
        return FALLBACK_RESPONSES.get(difficulty, FALLBACK_RESPONSES["beginner"])
    if any(w in msg_lower for w in ["hadamard", " h gate"]):
        return "The Hadamard gate creates equal superposition: it maps |0⟩ → ½(|0⟩+|1⟩) and |1⟩ → ½(|0⟩-|1⟩). Think of it as a quantum coin flip that leaves the coin spinning."
    if "entangle" in msg_lower:
        return "Quantum entanglement links two qubits so that measuring one instantly determines the state of the other, no matter how far apart they are. It's created by combining a Hadamard gate with a CNOT gate."
    if "grover" in msg_lower:
        return "Grover's algorithm searches an unsorted database of N items in O(√N) steps, compared to O(N) classically — a quadratic speedup. It works by amplifying the amplitude of the target state through repeated oracle + diffusion steps."
    return "That's a great quantum computing question! To get full AI-powered answers, add your OpenRouter API key to the backend .env file. I can explain any quantum concept, gate, or algorithm in depth."
