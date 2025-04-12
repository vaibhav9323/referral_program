# Django Referral Program Application

## Overview

This project implements a simple user referral system using Django, PostgreSQL, and Docker:

* User Registration with unique referral code generation.
* Tracking of referrer/referee relationships.
* User Login using email and password, establishing a session.
* A protected home page accessible only after login.
* JWT token endpoints for potential API authentication.
* An endpoint (planned, not yet implemented) to view referred users.

The application is containerized using Docker and Docker Compose for easy setup and development.

## Prerequisites

* Docker ([https://www.docker.com/get-started](https://www.docker.com/get-started))
* Docker Compose (usually included with Docker Desktop)

## Setup

1.  **Clone the Repository:** (If applicable)
    ```bash
    git clone <your-repository-url>
    cd referral_program
    ```
    Or navigate to your existing project directory (`E:\Study\python\referral_program`).

2.  **Create Environment File (`.env`):**
    Create a file named `.env` in the project root directory. Copy the content below and **replace placeholder values** with your actual database password and Django secret key.
    ```dotenv
    # .env

    # Database Settings
    POSTGRES_DB=referral_db
    POSTGRES_USER=referral_user
    POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD # Replace with your secure password
    DB_HOST=db # Matches the db service name in docker-compose/local.yml
    DB_PORT=5432

    # Django Settings
    SECRET_KEY='YOUR_DJANGO_SECRET_KEY' # Replace with your actual secret key
    DEBUG=True # Set to False for production
    ```

3.  **Add `.env` to `.gitignore`:**
    Ensure your `.gitignore` file (create one if it doesn't exist) includes `.env` to prevent committing sensitive information:
    ```gitignore
    # .gitignore
    .env
    __pycache__/
    *.pyc
    # Add other patterns like virtual env folders if needed
    ```

4.  **Review Configuration:**
    * Ensure `settings.py` reads database credentials, `SECRET_KEY`, and `DEBUG` from environment variables using `os.environ.get()` [cite: uploaded:referral_program/settings.py].
    * Ensure `docker-compose.yml` and `local.yml` use `env_file: - .env` for the `app` service and pass necessary variables to the `db` service environment [cite: uploaded:referral_program/docker-compose.yml, uploaded:referral_program/local.yml].
    * Ensure `Dockerfile` uses `/app` consistently for `WORKDIR` and `COPY` destinations, matching the volume mount in the compose files [cite: uploaded:referral_program/Dockerfile, uploaded:referral_program/docker-compose.yml].

## Running the Application (Development)

This uses the `local.yml` file, which automatically starts the Django development server.

1.  **Build Docker Images:** (Needed initially or after `Dockerfile`/`requirements.txt` changes)
    ```bash
    docker-compose -f local.yml build
    ```

2.  **Run Database Migrations:** (Crucial before first run or after model changes)
    * Ensure the database container is running. You might need to start it separately first if running migrations before the app: `docker-compose -f local.yml up -d db`
    * Run migrations using the `app` service definition:
        ```bash
        # Run migrations using a temporary container based on the app service
        docker-compose -f local.yml run --rm app python manage.py migrate
        ```
        *Alternatively, if using `docker-compose.yml` with `command: sleep infinity`:*
        ```bash
        # docker-compose up -d
        # docker-compose exec app python manage.py migrate
        # docker-compose down # Stop if needed before using local.yml
        ```

3.  **Start Application & Database:**
    ```bash
    docker-compose -f local.yml up -d
    ```
    The application should now be running and accessible at [http://localhost:8000](http://localhost:8000).

4.  **Stopping the Application:**
    ```bash
    docker-compose -f local.yml down
    ```

## Running Management Commands

To run other Django `manage.py` commands (like `createsuperuser`, `makemigrations`, `check`, etc.):

1.  Ensure containers are running: `docker-compose -f local.yml up -d`
2.  Use `docker-compose exec`:
    ```bash
    docker-compose -f local.yml exec app python manage.py <your_command>
    # Examples:
    # docker-compose -f local.yml exec app python manage.py makemigrations app
    # docker-compose -f local.yml exec app python manage.py createsuperuser
    # docker-compose -f local.yml exec app python manage.py check
    ```

## Key Features & URLs

* **Registration:** `http://localhost:8000/register/` [cite: uploaded:referral_program/app/urls.py]
* **Login:** `http://localhost:8000/` [cite: uploaded:referral_program/app/urls.py]
* **Home/Dashboard:** `http://localhost:8000/home/` (Requires login) [cite: uploaded:referral_program/app/urls.py, uploaded:referral_program/app/views.py]
* **JWT Token Obtain:** `http://localhost:8000/api/token/` (POST email/password) [cite: uploaded:referral_program/urls.py]
* **JWT Token Refresh:** `http://localhost:8000/api/token/refresh/` (POST refresh token) [cite: uploaded:referral_program/urls.py]
* **Referral View:** (Not yet implemented)

## Technology Stack

* **Backend:** Django [cite: uploaded:referral_program/requirements.txt]
* **Database:** PostgreSQL [cite: uploaded:referral_program/docker-compose.yml]
* **Authentication:** Django Sessions (`@login_required`), JWT (`djangorestframework-simplejwt`) [cite: uploaded:referral_program/requirements.txt, uploaded:referral_program/settings.py]
* **Containerization:** Docker, Docker Compose
* **WSGI Server (Production):** Gunicorn [cite: uploaded:referral_program/requirements.txt]
