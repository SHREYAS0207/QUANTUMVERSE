.PHONY: dev build test seed clean

# Development
dev:
	docker compose up db -d
	@echo "Starting backend..."
	cd backend && uvicorn app.main:app --reload &
	@echo "Starting frontend..."
	cd frontend && npm run dev

# Docker full stack
build:
	docker compose up --build -d

# Seed the database
seed:
	cd backend && python seed.py

# Run tests
test:
	cd backend && pytest tests/ -v

# Stop everything
stop:
	docker compose down

# Clean volumes
clean:
	docker compose down -v --remove-orphans

# Check backend health
health:
	curl -s http://localhost:8000/health | python3 -m json.tool

# View logs
logs:
	docker compose logs -f backend
