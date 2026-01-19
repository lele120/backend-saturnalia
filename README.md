# Saturnalia Backend

Backend API per la gestione di vigneti, dati satellitari e previsioni vino, costruito con FastAPI, SQLAlchemy e PostGIS.

## Caratteristiche

- API RESTful per vigneti, indici satellitari e previsioni vino
- Integrazione PostGIS per geometrie geospatiali
- Cache TTL per prestazioni ottimali
- Logging per monitoraggio query
- Test unitari e di integrazione

## Setup

### Prerequisiti

- Python 3.11+
- PostgreSQL 17 con PostGIS
- Git

### Installazione

1. Clona il repository:
   ```bash
   git clone <repository-url>
   cd backend-saturnalia
   ```

2. Crea ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

3. Installa dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura database:
   - Assicurati PostgreSQL sia in esecuzione
   - Crea database: `createdb saturnalia`
   - Aggiorna `.env` con le tue credenziali:
     ```
     DATABASE_URL=postgresql://postgres:password@localhost/saturnalia
     DEBUG=false
     SECRET_KEY=your_secret_key
     ALLOWED_ORIGINS=http://localhost:3000
     ```

5. Inizializza tabelle:
   ```bash
   python -c "
   import asyncio
   from app.models import user, item, vineyard, satellite_index, wine_prediction
   from app.database.database import engine, Base
   async def init():
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)
   asyncio.run(init())
   "
   ```

6. Avvia server:
   ```bash
   uvicorn app.main:app --reload
   ```

L'API sarà disponibile su http://localhost:8000

## API Endpoints

### Vigneti (Vineyards)

#### GET /vineyards/area
Restituisce nome e area in ettari di un vigneto.

**Query Parameters:**
- `code` (string, required): Codice UUID del vigneto

**Esempio:**
```bash
curl "http://localhost:8000/vineyards/area?code=00e885e1-617f-4f97-99a6-ad4e59d30d55"
```

**Risposta:**
```json
{
  "name": "Château Sample",
  "hectares": 87.91757981929779
}
```

#### GET /vineyards/vigor
Restituisce nome e media NDVI (vigore) del vigneto.

**Query Parameters:**
- `code` (string, required): Codice UUID del vigneto

**Esempio:**
```bash
curl "http://localhost:8000/vineyards/vigor?code=00e885e1-617f-4f97-99a6-ad4e59d30d55"
```

**Risposta:**
```json
{
  "name": "Château Sample",
  "avg_vigor": 0.615
}
```

#### GET /vineyards/prediction
Restituisce previsione qualità vino per vigneto e anno.

**Query Parameters:**
- `code` (string, required): Codice UUID del vigneto
- `year` (integer, required): Anno di vendemmia

**Esempio:**
```bash
curl "http://localhost:8000/vineyards/prediction?code=00e885e1-617f-4f97-99a6-ad4e59d30d55&year=2025"
```

**Risposta:**
```json
{
  "id": 1,
  "vintage_year": 2025,
  "quality_score": 94,
  "market_price_est": 120.5
}
```

### Altri Endpoints

- GET /: Messaggio di benvenuto
- Endpoints per users e items (ereditati dal template)

## Struttura Progetto

```
backend-saturnalia/
├── app/
│   ├── config.py          # Configurazioni centralizzate
│   ├── database/
│   │   └── database.py    # Connessione DB e setup
│   ├── models/            # Modelli SQLAlchemy
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── vineyard.py
│   │   ├── satellite_index.py
│   │   └── wine_prediction.py
│   ├── repositories/      # Data access layer
│   │   ├── vineyard_repository.py
│   │   └── ...
│   ├── services/          # Business logic
│   │   ├── vineyard_service.py
│   │   └── ...
│   ├── schemas/           # Pydantic schemas
│   │   └── vineyard.py
│   ├── routers/           # API routes
│   │   ├── vineyard.py
│   │   └── ...
│   └── main.py            # App FastAPI
├── tests/                 # Test suite
│   ├── conftest.py
│   └── test_vineyard.py
├── requirements.txt       # Dipendenze
├── pytest.ini            # Config test
├── .env                  # Variabili ambiente
└── README.md
```

## Test

Esegui test:
```bash
pytest
```

Per test specifici:
```bash
pytest tests/test_vineyard.py -v
```

## Documentazione API

Visita http://localhost:8000/docs per la documentazione interattiva Swagger UI con esempi, descrizioni dettagliate e possibilità di testare gli endpoint direttamente.

Alternativa: http://localhost:8000/redoc per documentazione ReDoc.

## Logging

Il sistema logga:
- Query SQL eseguite (INFO)
- Query lente (>1s) (WARNING)
- Errori e eccezioni

Log configurati in `app/main.py`.

## Sicurezza

- CORS configurato per origini consentite
- Validazione input con Pydantic
- Gestione errori strutturata
- Secrets gestiti via variabili ambiente

## Contributi

1. Crea branch per feature
2. Scrivi test per nuove funzionalità
3. Aggiorna documentazione
4. Crea pull request

## Licenza

[Inserisci licenza se applicabile]