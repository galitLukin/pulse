# Pulse

Pulse monitors the real-time health of production data using read replicas.

## Goals

- Detect broken data within minutes
- Never impact production load
- Be quiet, predictable, and safe

## Project Structure

```
pulse/
├── backend/          # Python FastAPI backend
│   ├── app/          # Application code
│   │   ├── main.py   # FastAPI app entrypoint
│   │   ├── config.py # Environment variables & settings
│   │   ├── db/       # Database connections (Pulse DB & replicas)
│   │   ├── models/   # Data models (core & API)
│   │   ├── services/ # Business logic (scheduler, checker, alerts, etc.)
│   │   ├── api/      # REST API endpoints
│   │   ├── workers/  # Background job workers
│   │   ├── utils/    # Utility functions
│   │   └── startup.py # App startup hooks
│   ├── migrations/   # SQL database migrations
│   ├── tests/        # Test files
│   ├── scripts/      # Utility scripts
│   └── requirements.txt
├── frontend/         # React/Next.js frontend (to be implemented)
└── README.md
```

## Backend Setup

The backend is built with Python 3.11, FastAPI, and APScheduler.

### Prerequisites

- Python 3.11+
- PostgreSQL (for Pulse internal database)
- Access to customer read replicas (PostgreSQL)

### Installation

1. Navigate to backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:

```bash
# Apply migrations to your Pulse database
psql $PULSE_DATABASE_URL -f migrations/001_init.sql
psql $PULSE_DATABASE_URL -f migrations/002_add_alerts.sql
```

6. Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/tables` - List monitored tables
- `POST /api/tables` - Create a monitored table
- `GET /api/connections` - List database connections
- `POST /api/connections` - Create a database connection
- `GET /api/alerts` - List alerts

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Running Workers Manually

```bash
cd backend
python scripts/run_worker.py <table_id>
```

## Frontend

Frontend implementation coming soon (React + Next.js).
