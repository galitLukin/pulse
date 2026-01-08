-- Initial schema for Pulse internal database

-- Connections table (customer database replicas)
CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    connection_string TEXT NOT NULL,
    max_queries_per_minute INTEGER DEFAULT 60,
    max_concurrent_queries INTEGER DEFAULT 5,
    query_timeout_seconds INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tables table (monitored tables)
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    connection_id INTEGER NOT NULL REFERENCES connections(id) ON DELETE CASCADE,
    schema_name VARCHAR(255) NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    monitor_types TEXT[] NOT NULL, -- Array of monitor types: ['freshness', 'volume', 'schema']
    time_column VARCHAR(255), -- Required for freshness monitor
    check_interval_minutes INTEGER DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(connection_id, schema_name, table_name)
);

-- Checks table (health check results)
CREATE TABLE checks (
    id SERIAL PRIMARY KEY,
    table_id INTEGER NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    monitor_type VARCHAR(50) NOT NULL, -- 'freshness', 'volume', 'schema'
    status VARCHAR(50) NOT NULL, -- 'success', 'failure', 'error', 'skipped'
    result_data JSONB,
    error_message TEXT,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_checks_table_id ON checks(table_id);
CREATE INDEX idx_checks_executed_at ON checks(executed_at DESC);

-- Alerts table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    table_id INTEGER NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    monitor_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'resolved', 'suppressed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_alerts_table_id ON alerts(table_id);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at DESC);

-- Users table (for auth - MVP)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workspaces table (for multi-tenant support)
CREATE TABLE workspaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workspace users (many-to-many)
CREATE TABLE workspace_users (
    workspace_id INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (workspace_id, user_id)
);

-- Add workspace_id to connections and tables
ALTER TABLE connections ADD COLUMN workspace_id INTEGER REFERENCES workspaces(id) ON DELETE CASCADE;
ALTER TABLE tables ADD COLUMN workspace_id INTEGER REFERENCES workspaces(id) ON DELETE CASCADE;

CREATE INDEX idx_connections_workspace_id ON connections(workspace_id);
CREATE INDEX idx_tables_workspace_id ON tables(workspace_id);

