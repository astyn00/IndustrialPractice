from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import psycopg2
import os
from dotenv import load_dotenv
import asyncio
from notifier import send_telegram_alert

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Simplified initialization - This is now correct because the Dockerfile handles the server type
socketio = SocketIO(app)


# --- Database Connection ---
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Uses the DATABASE_URL environment variable when deployed on Render.
    """
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Fallback for local testing if DATABASE_URL isn't set, using .env
        print("DATABASE_URL not found, falling back to local .env configuration.")
        password = os.getenv('DB_PASSWORD')
        if not password:
            raise ValueError("DB_PASSWORD must be set in .env for local testing.")
        return psycopg2.connect(host="localhost", database="bolashak_energy", user="postgres", password=password)
    
    # Use the full URL provided by the deployment environment (Render)
    return psycopg2.connect(database_url)


# --- API Endpoints ---
@app.route('/')
def index():
    """Serves the live monitoring dashboard HTML page."""
    return render_template('index.html')

@app.route('/api/readings', methods=['POST'])
def add_reading():
    """
    Receives a new sensor reading, saves it to the database,
    and emits real-time events.
    """
    data = request.get_json()
    if not data or 'sensor_id' not in data or 'energy_kwh' not in data:
        return jsonify({"error": "Invalid data provided"}), 400

    socketio.emit('new_reading', data)

    # Advanced critical event analysis
    is_critical = False
    reason = None
    energy = data.get('energy_kwh', 0)
    status = data.get('status')

    if status == 'error':
        is_critical = True
        reason = f"Sensor reported 'error' status."
    elif energy > 450:
        is_critical = True
        reason = f"Energy level high: {energy} kWh (Threshold: >450)"

    data['reason'] = reason
    
    if is_critical:
        app.logger.info(f"CRITICAL EVENT: {reason}")
        socketio.emit('critical_event', data)
        alert_message = f"⚠️ CRITICAL ALERT ⚠️\nSensor: {data['sensor_id']}\nReason: {reason}"
        asyncio.run(send_telegram_alert(alert_message))

    # Save to database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sensor_readings (sensor_id, timestamp, energy_kwh, status, is_critical) VALUES (%s, %s, %s, %s, %s)",
            (data['sensor_id'], data['timestamp'], energy, status, is_critical)
        )
        conn.commit()
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Could not save to database"}), 500
    finally:
        if 'cur' in locals() and cur: cur.close()
        if 'conn' in locals() and conn: conn.close()

    return jsonify({"message": "Reading processed successfully"}), 201


if __name__ == '__main__':
    print("Starting Flask-SocketIO development server on http://127.0.0.1:5000")
    # This runs the app for local development
    socketio.run(app, debug=True, port=5000)