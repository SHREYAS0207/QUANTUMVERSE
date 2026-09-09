# QuantumVerse — API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | /auth/register | email, username, password | Create account |
| POST | /auth/login | email, password | Get JWT tokens |
| POST | /auth/refresh | refresh_token | Refresh access token |
| GET | /auth/me | — | Current user profile |

## Circuits
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /circuits | List user's circuits |
| POST | /circuits | Save new circuit |
| GET | /circuits/{id} | Get circuit |
| PUT | /circuits/{id} | Update circuit |
| DELETE | /circuits/{id} | Delete circuit |

## Simulation
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | /simulation/run | gates, num_qubits, shots | Run simulation |
| POST | /simulation/step | gates, step_index | Step-by-step |
| GET | /simulation/{id} | — | Get result |

## Algorithms
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /algorithms | List all algorithms |
| POST | /algorithms/grover | Run Grover's search |
| POST | /algorithms/qft | Run QFT |
| POST | /algorithms/deutsch | Run Deutsch-Jozsa |
| POST | /algorithms/teleport | Run teleportation |

## Learning
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /learning/modules | List all modules |
| GET | /learning/modules/{id} | Module + lessons |
| POST | /learning/progress | Mark lesson complete |
| GET | /learning/progress | Get user progress |

## AI Tutor
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | /ai-tutor/chat | message, session_id | Chat with tutor |
| POST | /ai-circuit/generate | description | AI → circuit JSON |

## Quiz
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /quiz/{module_id} | Get quiz questions |
| POST | /quiz/submit | Submit answers |

## Achievements
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /achievements | All achievements |
| GET | /achievements/user | User's earned badges |
