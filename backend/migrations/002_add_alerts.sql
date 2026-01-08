-- Additional indexes and optimizations for alerts

-- Index for active alerts query
CREATE INDEX idx_alerts_active ON alerts(table_id, status) 
WHERE status = 'active';

-- Index for recent checks per table
CREATE INDEX idx_checks_recent ON checks(table_id, monitor_type, executed_at DESC);

