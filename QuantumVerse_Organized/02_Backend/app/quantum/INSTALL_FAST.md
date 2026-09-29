# Fast Install

Copy these folders into your existing QuantumVerse project:

```bash
cp -R frontend/src/app/ai-tutor ../QuantumVerse_Organized/01_Frontend/src/app/
cp -R frontend/src/app/quantum-solver ../QuantumVerse_Organized/01_Frontend/src/app/
cp -R frontend/src/app/quantum-explorer ../QuantumVerse_Organized/01_Frontend/src/app/
cp -R frontend/src/components/qlearn ../QuantumVerse_Organized/01_Frontend/src/components/
cp frontend/src/services/qlearnService.ts ../QuantumVerse_Organized/01_Frontend/src/services/
cp frontend/src/types/qlearn.ts ../QuantumVerse_Organized/01_Frontend/src/types/
cp -R backend/app/qlearn ../QuantumVerse_Organized/02_Backend/app/
cp backend/app/api/v1/qlearn.py ../QuantumVerse_Organized/02_Backend/app/api/v1/
cp backend/app/schemas/qlearn.py ../QuantumVerse_Organized/02_Backend/app/schemas/
cp backend/app/models/qlearn.py ../QuantumVerse_Organized/02_Backend/app/models/
```

Then add this to your backend API router:

```python
from app.api.v1.qlearn import router as qlearn_router
api_router.include_router(qlearn_router, prefix="/qlearn", tags=["qlearn"])
```

Run database migration:

```bash
psql "$DATABASE_URL" -f database/001_qlearn_three_features.sql
```
