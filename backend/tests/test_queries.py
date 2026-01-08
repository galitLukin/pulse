"""
Tests for safe queries
"""

import pytest
from app.db.queries import SafeQueries


def test_safe_queries_initialization():
    """Test that SafeQueries has expected methods"""
    queries = SafeQueries()
    
    assert hasattr(queries, 'check_freshness')
    assert hasattr(queries, 'check_volume')
    assert hasattr(queries, 'check_schema')
    assert hasattr(queries, 'check_replica_lag')
    assert hasattr(queries, 'check_zero_rows')


# TODO: Add integration tests with test database

