# Real-Time Industrial Monitoring & Alerting System

| Live Demo |
|---|
| **https://industrialpractice.onrender.com** |

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)

This project is a comprehensive, full-stack monitoring and alerting system developed for the Industrial Practice course at Astana IT University. It simulates a real-time data pipeline for an industrial setting (e.g., `ТОО «Болашақ Энергиясы»`), demonstrating a complete development lifecycle from data ingestion and processing to live multi-channel user notification and cloud deployment.

## Key Features

-   **Backend API**: A robust API built with **Python** and **Flask** to receive and process sensor data.
-   **Real-Time Dashboard**: A live, single-page web application built with **HTML/JS** that uses **WebSockets (Flask-SocketIO)** to display all incoming sensor readings and critical alerts without needing a page refresh. Includes a light/dark theme switcher.
-   **Multi-Channel Alerting**: In addition to the dashboard, the system sends instant push notifications for critical events via a **Telegram Bot**, demonstrating third-party API integration.
-   **Data Persistence**: All readings are stored in a cloud-hosted **PostgreSQL** database, with critical events flagged for easy querying.
-   **Cloud Deployment**: The entire application is containerized using **Docker** and deployed to **Render**, making it globally accessible and scalable.
-   **Secure Configuration**: Utilizes environment variables for managing sensitive credentials like database connection strings and API tokens, both locally and in the cloud.
-   **Automated Testing**: Includes a suite of unit tests written with **pytest** to validate the core business logic.

## System Architecture

The system operates as a distributed application:
1.  A local `collector` script simulates sensor data and sends it over the internet to the deployed API endpoint.
2.  The cloud-hosted Flask API receives the data, analyzes it for critical conditions (e.g., error status, high energy readings), and saves it to the cloud PostgreSQL database.
3.  The API uses **WebSockets** to push every new reading to all connected dashboard clients anywhere in the world.
4.  If an event is deemed critical, the API simultaneously:
    -   Emits a specific WebSocket event to the "Critical Alerts" panel on the dashboard, including the reason for the alert.
    -   Sends a formatted alert message via the Telegram Bot API to a specified user or channel.

## Local Development Setup

To run a copy of this project on a local machine for development or testing, follow these steps.

### 1. Prerequisites
-   Python 3.9+
-   PostgreSQL
-   Git

### 2. Clone the Repository
git clone https://github.com/astyn00/IndustrialPractice.git
cd IndustrialPractice

### 3. Setup Local Environment

Create and activate a Python virtual environment:


python -m venv venv
.\venv\Scripts\activate


Install the required dependencies:

pip install -r requirements.txt


Create a file named .env in the project root and add your local credentials:


DB_PASSWORD="your_local_postgres_password"
TELEGRAM_BOT_TOKEN="your_bot_token"
TELEGRAM_CHAT_ID="your_chat_id"

### 4. Running the System Locally

You will need two terminals running simultaneously.

Terminal 1: Start the Local API Server

Generated bash
# Make sure your virtual environment is active
python api/app.py


The server will start on http://127.0.0.1:5000.

Terminal 2: Run the Data Collector

Generated bash
# Make sure your virtual environment is active
python data_collector/collector.py


Note: To test the local server, ensure the API_URL in collector.py is set to http://127.0.0.1:5000/api/readings.

### 5. Running Tests

To run the unit tests, execute the following command in your terminal (with the virtual environment active):

pytest

### 6. Deployment 
This application is containerized with Docker and deployed on Render. The live, publicly accessible dashboard can be viewed at the link below.
Live Application URL: https://industrialpractice.onrender.com
