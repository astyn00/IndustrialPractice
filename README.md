# Real-Time Industrial Monitoring & Alerting System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)

This project is a comprehensive backend system developed for the Industrial Practice course at Astana IT University. It simulates a real-time monitoring and alerting platform for an industrial setting, such as the one at `ТОО «Болашақ Энергиясы»`.

The system is designed to ingest time-series data from sensors, process it, identify critical events, persist the data for analysis, and provide immediate, multi-channel notifications.

## Key Features

-   **Backend API**: A robust API built with **Python** and **Flask** to receive and process sensor data.
-   **Real-Time Dashboard**: A live, single-page web application built with **HTML/JS** that uses **WebSockets (Flask-SocketIO)** to display all incoming sensor readings and critical alerts without needing a page refresh. Includes a light/dark theme switcher.
-   **Multi-Channel Alerting**: In addition to the dashboard, the system sends instant push notifications for critical events via a **Telegram Bot**, demonstrating third-party API integration.
-   **Data Persistence**: All readings are stored in a **PostgreSQL** database, with critical events flagged for easy querying.
-   **Containerization**: The entire application is containerized using **Docker**, ensuring consistency across development and deployment environments.
-   **Secure Configuration**: Utilizes environment variables (`.env`) for managing sensitive credentials like database passwords and API tokens.
-   **Automated Testing**: Includes a suite of unit tests written with **pytest** to validate the core business logic.

## System Architecture

The system operates as follows:
1.  A `collector` script simulates sensor data and sends it to the API.
2.  The Flask API receives the data, analyzes it, and saves it to the PostgreSQL database.
3.  If an event is critical, the API simultaneously:
    -   Emits a WebSocket event to all connected dashboard clients with details about the event and the reason it was flagged.
    -   Sends a formatted alert message via the Telegram Bot API to a specified user or channel.

## Local Development & Testing

Follow these steps to run the project on your local machine.

#### 1. Prerequisites
-   Python 3.9+
-   PostgreSQL
-   Git

#### 2. Clone the Repository
```bash
# Replace with your own GitHub username and repository name
git clone https://github.com/astyn00/IndustrialPractice.git
cd IndustrialPractice
### 3. Setup Environment
# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the project root and add your credentials
# DB_PASSWORD="your_local_postgres_password"
# TELEGRAM_BOT_TOKEN="your_bot_token"
# TELEGRAM_CHAT_ID="your_chat_id"

#### 4. Run the System
You will need two terminals.
Terminal 1: Start the API Server
# Make sure your virtual environment is active
python api/app.py
The server will start on http://127.0.0.1:5000
Terminal 2: Run the Data Collector
# Make sure your virtual environment is active
python data_collector/collector.py
Now, open http://127.0.0.1:5000 in your browser to see the live dashboard in action.
#### Running Tests
To run the unit tests, execute the following command in your terminal (with the virtual environment active):
pytest
