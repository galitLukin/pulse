"""
Tests for checker service
"""

import pytest
from app.services.checker import CheckerService
from app.models.core import MonitorType


def test_checker_service_initialization():
    """Test that checker service initializes correctly"""
    service = CheckerService()
    assert service is not None
    assert service.baseline_service is not None
    assert service.queries is not None


# TODO: Add more tests for check execution, error handling, etc.

