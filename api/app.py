from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import psycopg2
import os
from dotenv import load_dotenv
import asyncio
from notifier import send_telegram_alert

load_dotenv()
app = Flask(__name__)
# This works for both local dev and Gunicorn/Eventlet in Docker
socketio = SocketIO(app, async_mode='eventlet')

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Uses the DATABASE_URL environment variable when deployed on Render.
    """
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Fallback for local testing if DATABASE_URL isn't set
        print("DATABASE_URL not found, falling back to local .env configuration.")
        password = os.getenv('DB_PASSWORD')
        return psycopg2.connect(host="localhost", database="bolashak_energy", user="postgres", password=password)
    
    # Use the full URL provided by the deployment environment
    return psycopg2.connect(database_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/readings', methods=['POST'])
def add_reading():
    data = request.get_json()
    if not data or 'sensor_id' not in data or 'energy_kwh' not in data: return jsonify({"error": "Invalid data"}), 400
    
    socketio.emit('new_reading', data)
    
    is_critical, reason = False, None
    energy = data.get('energy_kwh', 0)
    status = data.get('status')

    if status == 'error': is_critical, reason = True, "Sensor reported 'error' status."
    elif energy > 450: is_critical, reason = True, f"Energy level high: {energy} kWh"
    
    data['reason'] = reason
    if is_critical:
        socketio.emit('critical_event', data)
        alert_message = f"⚠️ CRITICAL ALERT ⚠️\nSensor: {data['sensor_id']}\nReason: {reason}"
        asyncio.run(send_telegram_alert(alert_message))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sensor_readings (sensor_id, timestamp, energy_kwh, status, is_critical) VALUES (%s, %s, %s, %s, %s)",
            (data['sensor_id'], data['timestamp'], status, energy, is_critical)
        )
        conn.commit()
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "DB save failed"}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

    return jsonify({"message": "Processed"}), 201

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)