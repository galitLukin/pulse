"""
Tests for alert service
"""

import pytest
from app.services.alerts import AlertService
from app.models.core import MonitorType, CheckStatus


def test_alert_service_initialization():
    """Test that alert service initializes correctly"""
    service = AlertService()
    assert service is not None


def test_should_alert_on_consecutive_failures():
    """Test that alerts are created after threshold failures"""
    service = AlertService()
    table_id = 1
    monitor_type = MonitorType.VOLUME
    
    # First failure - should not alert
    assert not service.should_alert(table_id, monitor_type, CheckStatus.FAILURE, threshold=2)
    
    # Second failure - should alert
    assert service.should_alert(table_id, monitor_type, CheckStatus.FAILURE, threshold=2)
    
    # Success resets counter
    service.should_alert(table_id, monitor_type, CheckStatus.SUCCESS, threshold=2)
    assert not service.should_alert(table_id, monitor_type, CheckStatus.FAILURE, threshold=2)

