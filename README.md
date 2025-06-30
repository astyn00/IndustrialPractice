# Data Monitoring System for Industrial Practice

This project is a backend data monitoring system developed as part of the Industrial Practice for the Computer Science program at Astana IT University. The system is designed to simulate the collection, processing, and storage of energy sensor data from an industrial environment at ТОО «Болашақ Энергиясы».

## Core Features

-   **Data Simulation:** A Python script generates realistic, time-series sensor data.
-   **Backend API:** A RESTful API built with Python and Flask receives and processes incoming data.
-   **Data Persistence:** Sensor readings are stored and managed in a PostgreSQL database.
-   **Validation Logic:** The API includes logic to validate incoming data and flag critical readings (e.g., based on status or high energy values).
-   **Secure Configuration:** Uses environment variables (`.env` file) to manage sensitive information like database credentials, following best practices.
-   **Unit Testing:** Includes unit tests written with `pytest` to ensure the reliability of the core business logic.

## Technology Stack

-   **Backend:** Python 3.9+
-   **API Framework:** Flask
-   **Database:** PostgreSQL
-   **Database Driver:** `psycopg2`
-   **Testing:** `pytest`
-   **Version Control:** Git

## Project Structure
/data-monitoring-system/
│
├── api/
│ └── app.py # Main Flask API server
│
├── data_collector/
│ ├── collector.py # Script to send data to the API
│ └── data_generator.py # Script to simulate sensor data
│
├── database/
│ └── setup.sql # SQL script to create the database table
│
├── tests/
│ └── test_validation.py # Unit tests for the validation logic
│
├── .env # Environment variables (e.g., DB_PASSWORD)
├── .gitignore # Specifies files for Git to ignore
└── README.md # This documentation file


## Setup and Installation

Follow these steps to run the project locally.

1.  **Prerequisites:**
    -   Python 3.9+
    -   PostgreSQL
    -   Git

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/data-monitoring-system.git
    cd data-monitoring-system
    ```

3.  **Set up the Database:**
    -   Create a new database in PostgreSQL named `bolashak_energy`.
    -   Run the `database/setup.sql` script in pgAdmin to create the `sensor_readings` table.

4.  **Create a Virtual Environment and Install Dependencies:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**
    -   Create a file named `.env` in the root directory.
    -   Add your PostgreSQL password to it:
        ```
        DB_PASSWORD="your_postgres_password"
        ```

## How to Run the System

You will need two terminals.

**Terminal 1: Start the API Server**
```bash
# Make sure your virtual environment is active
python api/app.py

# Make sure your virtual environment is active
python data_collector/collector.py