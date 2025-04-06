# Use an official Python runtime
FROM python:3.10-slim

# Set environment variables to prevent buffering and bytecode files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the (currently empty) app directory contents into the container
# Later, docker-compose will mount your local code here for development
COPY . /app/

# Expose port 8000 to allow communication with the app
EXPOSE 8000

# We will define the command to run the app in docker-compose.yml for now