# Base image
FROM python:3.11

ENV DJANGO_SETTINGS_MODULE=ast_rule_engine.settings
ENV PYTHONUNBUFFERED 1
RUN apt update -y
RUN apt install -y build-essential libpq-dev jq
RUN pip install --upgrade pip psycopg2 awscli poetry==1.7.1

# Set working directory inside the container
WORKDIR /code

# Copy Poetry configuration files and lock file
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install dependencies via Poetry
RUN poetry config virtualenvs.create false; poetry install --no-dev --no-interaction --no-ansi

# Copy the Django project code to the container
COPY . /code

# Expose the port Django will run on
EXPOSE 8000

# Run migrations and start the Django server
CMD ["poetry", "run", "python", "manage.py", "migrate"]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
