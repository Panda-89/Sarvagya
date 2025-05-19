# Cross-Platform System Utility + Admin Dashboard

## Project Overview

This project consists of a system utility that runs on multiple platforms (Windows, macOS, Linux) to collect system health data and report it to a backend server. The backend stores and exposes the data via REST APIs. A React-based admin dashboard provides a user interface to view and manage reports from multiple machines.

---

## Features

- **System Utility (Client):**
  - Checks disk encryption status, OS update status, antivirus presence, and inactivity sleep settings.
  - Runs as a background daemon checking system health periodically.
  - Sends data to backend only if changes are detected.

- **Backend Server:**
  - Receives and stores system reports in a SQLite database.
  - Provides REST API endpoints to:
    - Submit reports
    - List machines and their latest status
    - Filter machines by OS and issue status
    - Export data as CSV

- **Admin Dashboard (Frontend):**
  - Lists all reporting machines with their latest data.
  - Flags configuration issues (e.g., unencrypted disk, outdated OS).
  - Shows last check-in time.
  - Provides filters and sorting capabilities.

---

## Repository Structure
/Sarvagya-project-root
│
├── backend/ # Backend FastAPI server
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│ ├── requirements.txt
│
|__system_checks.py
|__daemon.py
└── frontend/ # React admin dashboard
 ├── package.json
 ├── public/
 ├── src/
 └── README.md

---

## Backend Setup

### Prerequisites

- Python 3.8+
- pip

### Steps

## 1. Navigate to the backend directory:


```bash
cd backend

## 2. Create and activate a virtual environment

python -m venv venv
# On Linux/macOS
source venv/bin/activate
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

## 3. Install the required Python packages:

pip install -r requirements.txt

## 4. Run the FastAPI backend server:

uvicorn backend.main:app --reload

The backend API will be available at: http://127.0.0.1:8000

API Endpoints
 POST /report
 Submit system health reports.

 GET /machines
 List all machines with their latest status.

 GET /machines?os=Windows&issue=disk_encryption
 Filter machines by OS or issue.

 GET /export/csv
 Export machine data as CSV file.


## Frontend Setup

Prerequisites
   Node.js (v14+ recommended)
   npm

Steps 
   1. Navigate to the frontend directory:
      cd frontend

   2. Install dependencies:
      npm install

   3. Start the react development server: 
      nom start

The dashboard will be accessible at http://localhost:3000


## Testing the System Utility

The daemon.py script simulates periodic checks and sends reports to the backend.

Run it with:
    python backend/daemon.py
Make sure the backend server is running before starting the daemon.



## Example cURL Requests

Submit a report:
  curl -X POST "http://127.0.0.1:8000/report" \
-H "Content-Type: application/json" \
-d '{
  "machine_id": "machine_1",
  "os": "Windows 10",
  "disk_encryption": true,
  "os_updates": true,
  "antivirus": true,
  "sleep_settings": true
}'

Get all machines 
   curl http://127.0.0.1:8000/machines

Export csv: 
   curl http://127.0.0.1:8000/export/csv --output machines.csv


## Notes 

The backend uses SQLite for simplicity. You can replace it with any other database if needed.

The system checks in system_checks.py are basic and partly simulated; you can extend them per platform.

CORS is enabled on backend to allow requests from the frontend (http://localhost:3000).