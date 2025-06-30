import random
import datetime

# This is a simple counter to keep track of how many times the function is called.
# We will use this to force a specific event during the demonstration.
call_count = 0

def generate_fake_reading():
    """
    Generates a single fake sensor reading.
    To ensure a critical event happens for the demonstration, this function
    is hardcoded to return a critical reading on the 5th call.
    """
    global call_count
    call_count += 1

    sensors = ["SENSOR_A-101", "SENSOR_B-205", "SENSOR_C-310"]
    
    # --- FORCED CRITICAL EVENT FOR DEMONSTRATION ---
    # On the 5th call, we force a critical event to ensure it appears on the dashboard.
    if call_count == 5:
        print(">>> FORCING A CRITICAL EVENT FOR DEMONSTRATION <<<")
        return {
            "sensor_id": "SENSOR-CRITICAL-TEST",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "energy_kwh": 499.99, # This value is > 450, making it critical
            "status": "error"
        }

    # --- REGULAR RANDOM DATA GENERATION ---
    # For all other calls, generate a normal or warning reading.
    # The probability of 'error' is set to 0 to avoid other random critical events.
    statuses = ["normal", "warning"]
    reading = {
        "sensor_id": random.choice(sensors),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "energy_kwh": round(random.uniform(100.0, 400.0), 2),
        "status": random.choices(statuses, weights=[85, 15], k=1)[0]
    }
    return reading

if __name__ == "__main__":
    # This part is just for testing the function by itself.
    # It's not used when collector.py imports it.
    print("Generated a sample sensor reading:")
    for i in range(10):
        print(f"Call {i+1}: {generate_fake_reading()}")