# Pulse Backend

Python FastAPI backend for real-time data health monitoring via read replicas.

## Tech Stack

- **Python 3.11**
- **FastAPI** - Web framework
- **APScheduler** - Background job scheduling
- **PostgreSQL** - Internal database (psycopg3)
- **psycopg3** - Database driver

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entrypoint
│   ├── config.py        # Environment variables & settings
│   ├── db/              # Database connections
│   │   ├── pulse_db.py  # Internal Pulse DB
│   │   ├── replica_db.py # Customer replica connections
│   │   └── queries.py   # Safe SQL queries
│   ├── models/          # Data models
│   │   ├── core.py      # Internal DB models
│   │   └── api.py       # Pydantic request/response models
│   ├── services/        # Business logic
│   │   ├── scheduler.py # Job scheduling
│   │   ├── checker.py   # Health check execution
│   │   ├── baselines.py # Rolling baselines
│   │   ├── alerts.py    # Alert management
│   │   └── safety.py    # Safety guardrails
│   ├── api/             # REST API endpoints
│   │   ├── health.py
│   │   ├── tables.py
│   │   ├── connections.py
│   │   └── alerts.py
│   ├── workers/         # Background workers
│   │   └── run_checks.py
│   ├── utils/           # Utilities
│   │   ├── time.py
│   │   ├── logging.py
│   │   └── retry.py
│   └── startup.py       # App startup hooks
├── migrations/          # SQL migrations
├── tests/               # Tests
├── scripts/             # Utility scripts
└── requirements.txt     # Dependencies
```

## Setup

See main [README.md](../README.md) for setup instructions.

## Key Features

- **Read-only replica connections** - Never touches production
- **Safety guardrails** - Query budgets, timeouts, rate limiting
- **Scheduled health checks** - APScheduler for periodic monitoring
- **Anomaly detection** - Rolling baselines for volume monitoring
- **Alert management** - Consecutive failure tracking, suppression

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/tables` - List monitored tables
- `POST /api/tables` - Create monitored table
- `GET /api/connections` - List database connections
- `POST /api/connections` - Create database connection
- `GET /api/alerts` - List alerts

## Development

Run the server:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest tests/
```

Run migrations:

```bash
psql $PULSE_DATABASE_URL -f migrations/001_init.sql
psql $PULSE_DATABASE_URL -f migrations/002_add_alerts.sql
```
