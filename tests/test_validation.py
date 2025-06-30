import pytest

# This is the function from our API that we want to test.
# By testing it separately, we don't need to run the whole server.
def is_reading_critical(reading):
    """Determines if a reading is critical based on its status or energy level."""
    if not isinstance(reading, dict):
        return False
    
    status = reading.get('status')
    energy = reading.get('energy_kwh', 0)
    
    if status == 'error':
        return True
    if energy > 450:
        return True
    
    return False

# --- The Tests ---

def test_critical_by_status():
    """Test if 'error' status is correctly identified as critical."""
    reading = {'status': 'error', 'energy_kwh': 200}
    assert is_reading_critical(reading) is True

def test_critical_by_energy():
    """Test if high energy level is correctly identified as critical."""
    reading = {'status': 'normal', 'energy_kwh': 500}
    assert is_reading_critical(reading) is True

def test_not_critical():
    """Test if a normal reading is correctly identified as not critical."""
    reading = {'status': 'normal', 'energy_kwh': 300}
    assert is_reading_critical(reading) is False

def test_boundary_case():
    """Test the boundary condition for energy level (450 should not be critical)."""
    reading = {'status': 'warning', 'energy_kwh': 450}
    assert is_reading_critical(reading) is False