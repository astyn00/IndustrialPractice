import requests
import time
from data_generator import generate_fake_reading

# The URL of our running Flask API
API_URL = "https://industrialpractice.onrender.com/api/readings"

def send_reading_to_api(reading):
    """Sends a single reading to the API via a POST request."""
    try:
        response = requests.post(API_URL, json=reading)
        if response.status_code == 201:
            print(f"Successfully sent reading for sensor {reading['sensor_id']}")
        else:
            print(f"Error sending reading. Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to the API at {API_URL}.")
        print("Is the Flask API server (app.py) running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Starting data collector...")
    print(f"Will send data to API at: {API_URL}")
    
    # We will send 10 readings, one every 2 seconds, to simulate a stream.
    for i in range(10):
        fake_reading = generate_fake_reading()
        send_reading_to_api(fake_reading)
        time.sleep(2)  # Wait for 2 seconds before sending the next one
    
    print("Data collection finished.")