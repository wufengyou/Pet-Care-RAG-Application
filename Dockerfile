FROM python:3.12-slim

WORKDIR /app

# Install pipenv, PostgreSQL client, and other dependencies
RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y postgresql-client

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile --system

# Install Streamlit
RUN pip install streamlit

# Copy the application code
COPY Pet_care_app .
COPY 2_data/updated_category.csv 2_data/updated_category.csv

# Copy database initialization script
COPY db_init.py .

# Copy Streamlit app
COPY pet_care_streamlit.py .

# Copy wait-for-postgres script
COPY wait_for_postgres.sh .
RUN chmod +x wait_for_postgres.sh

EXPOSE 5000 8501

# The command is now specified in docker-compose.yaml