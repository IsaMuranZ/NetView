# Netview 0.1.0

## Purpose

To create a fullstack application that can monitor, analyze, and document a network and provide a convenient UI for ease of access.

## Technologies

- **Backend:** Python, Flask
- **Frontend:** React, TypeScript
- **Database:** PostgreSQL

## Dependencies

- Python 3.8+ (including `venv` for virtual environments)
- Node.js and npm (for managing JavaScript dependencies)
- PostgreSQL (database)
- Git (for version control)

## Installation/Deployment

Follow these steps to set up, deploy, and run the application on a Linux machine.

### 1. Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/IsaMuranZ/NetView.git
cd NetView
```
### 2. Install System Dependencies

You'll need to install several system dependencies using your Linux package manager (e.g., `apt` for Debian-based systems):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm postgresql git
```
### 3. Set Up the Backend

#### 3.1. Create and Activate a Python Virtual Environment

It's recommended to use a Python virtual environment to manage dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3.2. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

#### 3.3. Set Up the PostgreSQL Database

You'll need to create a PostgreSQL user and database. Replace `netview_user`, `netviewadmin`, and `netview` with your desired username, password, and database name:

```bash
sudo -u postgres psql
CREATE USER netview_user WITH PASSWORD 'netviewadmin';
CREATE DATABASE netview;
GRANT ALL PRIVILEGES ON DATABASE netview TO netview_user;
\q
```

Update your Flask application's configuration with the correct database URI in `app/__init__.py` or through environment variables.

#### 3.4. Apply Database Migrations

If you have migrations set up, apply them:

```bash
flask db upgrade
```

### 4. Set Up the Frontend

#### 4.1. Install Node.js Dependencies

Navigate to the frontend directory and install the necessary packages:

```bash
cd frontend
npm install
```

#### 4.2. Build the Frontend

Build the React application:

```bash
npm run build
```

### 5. Running the Application

You can now run both the frontend and backend servers.

#### 5.1. Run the Flask Backend

From the root directory, start the Flask backend:

```bash
source .venv/bin/activate
export FLASK_APP=run.py
export FLASK_ENV=development  # Optional: for development mode
flask run
```

The Flask server should now be running on `http://localhost:5000`.

#### 5.2. Run the React Frontend

Navigate to the `frontend` directory and start the development server:

```bash
cd frontend
npm start
```

The React development server should now be running on `http://localhost:3000`.

### 6. Accessing the Application

You can access the application by navigating to `http://localhost:3000` in your web browser. The backend API is accessible at `http://localhost:5000`.

### 7. Using Netview

After minimal setup, run the network monitoring scripts to populate the database and web app with data.

```bash
cd /path/to/NetView
sudo PYTHONPATH=$PYTHONPATH:/path/to/NetView/ /path/to/NetView/.venv/bin/python scripts/continuous_monitoring.py
```

The scripts need super user privileges to gather network data. Replace /path/to/NetView with the path to where your working directory is. The script will run in the background collecting network data on connected devices and traffic.
