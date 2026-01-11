# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

import pytest
from esnodepy.engine.boundaries import FunctionBoundary

def test_boundary_initialization():
    """Test that a FunctionBoundary initializes correctly."""
    fb = FunctionBoundary("test_func", "int")
    assert fb.name == "test_func"
    assert fb.declared_return == "int"
    assert len(fb.observed_returns) == 0

def test_boundary_observation():
    """Test observing return types."""
    fb = FunctionBoundary("test_func", "int")
    fb.observe_return("int")
    assert "int" in fb.observed_returns
    assert not fb.has_drift()

def test_boundary_drift_detection():
    """Test correctly identifying drift (None return when something else declared)."""
    fb = FunctionBoundary("test_func", "int")
    fb.observe_return("None (implicit)")
    assert fb.has_drift()

def test_type_mismatch_is_not_drift_in_v02():
    """Ensure type mismatch ignores drift in v0.2 logic."""
    fb = FunctionBoundary("test_func", "int")
    fb.observe_return("str")
    assert not fb.has_drift()
    
def test_no_declared_return_drift():
    """Ensures no drift is reported if no return type is declared."""
    fb = FunctionBoundary("test_func", None)
    fb.observe_return("str")
    # If we didn't declare anything, we can't be drifting from it (in this simple model)
    assert not fb.has_drift()
