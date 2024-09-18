FROM python:3.12-slim

WORKDIR /app

# Install pipenv and PostgreSQL client
RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y postgresql-client

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile --system

# Copy the application code
COPY Pet_care_app .
COPY data/update_category.csv data/update_category.csv

# Copy database initialization script
COPY db_init.py .

# Copy wait-for-postgres script
COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

EXPOSE 5000

# The command is now specified in docker-compose.yaml
