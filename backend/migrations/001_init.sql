 /**
Initial schema for Pulse internal database
connections
    └── checks
            ├── check_runs (many)
            └── current_status (one)

Not doing yet:
Users / auth
Alerts
Organizations
Multi-tenant isolation
Credentials vault
Aggregates

To run migration: psql -h localhost -p 5432 -U pulse -d pulse -f migrations/001_init.sql
**/

-- Connections table (customer database replicas)
CREATE TABLE connections (
    id                      UUID PRIMARY KEY,
    connection_name         VARCHAR(255) NOT NULL,
    db_type                 TEXT NOT NULL,          -- postgres, mysql, etc (v1: postgres)
    host                    TEXT NOT NULL,
    port                    INTEGER NOT NULL,
    database_name           TEXT NOT NULL,

    max_queries_per_minute  INTEGER DEFAULT 60,
    max_concurrent_queries  INTEGER DEFAULT 5,
    query_timeout_seconds   INTEGER DEFAULT 2,
    is_active               BOOLEAN DEFAULT true,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Check configurations
CREATE TABLE checks (
    id                  UUID PRIMARY KEY,
    connection_id       UUID NOT NULL REFERENCES connections(id),

    check_type          TEXT NOT NULL,       -- e.g. 'replica_lag'
    config              JSONB NOT NULL,      -- thresholds, table names, etc

    interval_seconds    INTEGER NOT NULL DEFAULT 60,
    is_active           BOOLEAN NOT NULL DEFAULT true,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Check instances (append only) 
-- alerts, charts, and summaries are derived from this
CREATE TABLE check_runs (
    id              UUID PRIMARY KEY,
    check_id        UUID NOT NULL REFERENCES checks(id),

    started_at      TIMESTAMPTZ NOT NULL,
    finished_at     TIMESTAMPTZ NOT NULL,

    status          TEXT NOT NULL,   -- success | warning | error
    error_message   TEXT,

    metrics         JSONB,            -- lag_seconds, row_count, etc

    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- This is a derived table (latest state per check).
CREATE TABLE current_status (
    check_id        UUID PRIMARY KEY REFERENCES checks(id),

    status          TEXT NOT NULL,
    last_run_at     TIMESTAMPTZ NOT NULL,
    last_success_at TIMESTAMPTZ,

    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);