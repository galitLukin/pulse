 /**
Adding column + indexes

To run migration: psql -h localhost -p 5432 -U pulse -d pulse -f migrations/002_indexes.sql
**/

-- Add check_name column to checks table
ALTER TABLE checks ADD COLUMN check_name VARCHAR(255) NOT NULL DEFAULT 'Unnamed Check';

-- Remove the default after adding the column (for future inserts)
ALTER TABLE checks ALTER COLUMN check_name DROP DEFAULT;

-- Create indexes
CREATE INDEX idx_checks_connection ON checks(connection_id);
CREATE INDEX idx_check_runs_check_id ON check_runs(check_id);
CREATE INDEX idx_check_runs_created_at ON check_runs(created_at);
