# Django Referral Program Application

## Overview

This project implements a simple user referral system using Django, PostgreSQL, and Docker. It fulfills the requirements outlined in the "Backend Engineer Assignment" [cite: uploaded:Backend Engineer Assignment.pdf], including:

* User Registration with unique referral code generation [cite: uploaded:Backend Engineer Assignment.pdf].
* Tracking of referrer/referee relationships [cite: uploaded:Backend Engineer Assignment.pdf].
* User Login [cite: uploaded:Backend Engineer Assignment.pdf].
* An endpoint (planned, not yet implemented) to view referred users [cite: uploaded:Backend Engineer Assignment.pdf].
* JWT token endpoints for potential API authentication [cite: uploaded:referral_program/urls.py].

The application is containerized using Docker and Docker Compose for easy setup and deployment.

## Prerequisites

* Docker ([https://www.docker.com/get-started](https://www.docker.com/get-started))
* Docker Compose (usually included with Docker Desktop)

## Setup

1.  **Clone the Repository:** (Assuming this code is in a Git repository)
    ```bash
    git clone <your-repository-url>
    cd referral_program
    ```
    Or simply navigate to the project directory `E:\Study\python\referral_program`.

2.  **Create Environment File:** Create a file named `.env` in the project root directory by copying the example below. **Fill in your actual secure values** for `POSTGRES_PASSWORD` and `SECRET_KEY`.
    ```dotenv
    # .env

    # Database Settings
    POSTGRES_DB=referral_db
    POSTGRES_USER=referral_user
    POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD # Replace with a secure password
    DB_HOST=db # Service name in docker-compose.yml / local.yml
    DB_PORT=5432

    # Django Settings
    SECRET_KEY='YOUR_DJANGO_SECRET_KEY' # Replace with the key from settings.py or generate a new one
    DEBUG=True # Set to False in production
    ```
    **Important:** Add `.env` to your `.gitignore` file to prevent committing secrets.

3.  **Review Configuration:** Check the `Dockerfile`, `docker-compose.yml`, `local.yml`, and `settings.py` if needed [cite: uploaded:referral_program/Dockerfile, uploaded:referral_program/docker-compose.yml, uploaded:referral_program/local.yml, uploaded:referral_program/settings.py]. Ensure `settings.py` reads configuration from environment variables [cite: uploaded:referral_program/settings.py].

## Running the Application (Development)

This uses the `local.yml` file which automatically starts the Django development server.

1.  **Build the Docker images:**
    ```bash
    docker-compose -f local.yml build
    ```

2.  **Run Database Migrations:** Start the database container first, then run migrations inside the app container.
    ```bash
    # Start DB service temporarily (if not running)
    docker-compose -f local.yml up -d db

    # Run migrations inside a temporary app container or the main one if using sleep infinity in docker-compose.yml
    # Assuming you have the 'app' service defined in local.yml to build upon:
    docker-compose -f local.yml run --rm app python manage.py migrate
    # Or, if using the default docker-compose.yml with 'sleep infinity':
    # docker-compose up -d
    # docker-compose exec app python manage.py migrate
    # docker-compose down
    ```
    *(Ensure migrations are run at least once before starting the server for the first time)*

3.  **Start the Application and Database:**
    ```bash
    docker-compose -f local.yml up -d
    ```
    The application will be accessible at [http://localhost:8000](http://localhost:8000).

4.  **Stopping the Application:**
    ```bash
    docker-compose -f local.yml down
    ```

## Running Management Commands

To run commands like `makemigrations`, `migrate`, `createsuperuser`, etc., use `docker-compose exec`:

1.  Ensure containers are running (`docker-compose -f local.yml up -d`).
2.  Execute the command:
    ```bash
    docker-compose -f local.yml exec app python manage.py <your_command>
    # Example:
    # docker-compose -f local.yml exec app python manage.py makemigrations app
    # docker-compose -f local.yml exec app python manage.py createsuperuser
    ```

## Key Features & URLs

* **Registration:** `/register/` [cite: uploaded:referral_program/app/urls.py] - Renders and processes the registration form [cite: uploaded:referral_program/app/views.py].
* **Login:** `/` (Root URL) [cite: uploaded:referral_program/app/urls.py] - Renders and processes the login form [cite: uploaded:referral_program/app/views.py].
* **Home/Dashboard:** `/home/` [cite: uploaded:referral_program/app/urls.py] - Placeholder page after successful login, requires authentication [cite: uploaded:referral_program/app/views.py].
* **JWT Token Obtain:** `/api/token/` [cite: uploaded:referral_program/urls.py] - POST email/password to get JWT access/refresh tokens.
* **JWT Token Refresh:** `/api/token/refresh/` [cite: uploaded:referral_program/urls.py] - POST refresh token to get a new access token.
* **Referral View:** (To be implemented - as per original requirements [cite: uploaded:Backend Engineer Assignment.pdf])

## Technology Stack

* **Backend:** Django [cite: uploaded:referral_program/requirements.txt]
* **Database:** PostgreSQL [cite: uploaded:referral_program/docker-compose.yml]
* **Authentication:** Django Sessions (via `login_required`), JWT (via `djangorestframework-simplejwt`) [cite: uploaded:referral_program/requirements.txt]
* **Containerization:** Docker, Docker Compose
* **WSGI Server (for production):** Gunicorn [cite: uploaded:referral_program/requirements.txt]
