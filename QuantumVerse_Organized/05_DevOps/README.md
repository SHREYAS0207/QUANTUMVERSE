# QuantumVerse — DevOps & Infrastructure

## Files
```
docker-compose.yml    — Spins up frontend + backend + postgres + redis + nginx
Makefile              — Dev shortcuts (make dev, make build, make test …)
nginx/nginx.conf      — Reverse proxy config (port 80/443 → services)
github/workflows/
  ci.yml              — CI: lint + test on every PR
  deploy.yml          — CD: deploy to server on merge to main
```

## One-Command Start
```bash
cp 02_Backend/.env.example 02_Backend/.env     # fill in secrets
cp 01_Frontend/.env.local.example 01_Frontend/.env.local
docker compose -f 05_DevOps/docker-compose.yml up
```

## Services
| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js app |
| Backend | 8000 | FastAPI server |
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Cache + sessions |
| Nginx | 80 | Reverse proxy |

## Make Commands
```bash
make dev       # Start all services in dev mode
make build     # Build Docker images
make test      # Run all tests
make migrate   # Run Alembic migrations
make seed      # Seed the database
make clean     # Stop and remove containers
```
