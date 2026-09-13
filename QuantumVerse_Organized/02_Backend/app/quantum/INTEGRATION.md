# Integration Notes

This pack is intentionally modular and only adds the three requested QLearn systems. It uses your existing auth/app shell when copied into QuantumVerse.

Frontend pages are self-contained and call `/api/v1/qlearn/*`. Backend services perform deterministic quantum calculations for known core cases and return verified labels. Extend `backend/app/qlearn/quantum_math.py` for more gates, matrix parsing, and image OCR.
