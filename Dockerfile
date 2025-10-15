# Basic image
FROM python:3.11-slim

LABEL creator="Anton Galkin"

# Turn off interactive
ENV DEBIAN_FRONTEND=noninteractive

# creating user
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} docker_user && \
    useradd -m -u ${UID} -g ${GID} docker_user

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN python3.11 -m pip install uv==0.8.22

# Set working directory
WORKDIR /home/docker_user/app

# Copy uv lock file and project configuration
COPY uv.lock pyproject.toml ./

# Install dependencies using uv
RUN python3.11 -m uv pip install --no-cache-dir --system -r uv.lock

# Copying the entire project
COPY . .

# Fix permissions for docker_user before switching user
RUN chown -R docker_user:docker_user /home/docker_user/app

# switch to user
USER docker_user


# Under for use only Dockerfile without Docker Compose
# Create directories as docker_user
#RUN mkdir -p /home/docker_user/app/static && \
#    mkdir -p /home/docker_user/app/post/migrations

# Setting environment variables
#ENV PYTHONUNBUFFERED=1 \
#    DJANGO_SETTINGS_MODULE=django_weather_reminder.settings

# Running migrations and collecting static files (if SQLite only)
#RUN python3.11 manage.py makemigrations --no-input \
#    && python3.11 manage.py migrate \
#    && python3.11 manage.py collectstatic --no-input

# Open port
#EXPOSE 8000

# Command to run the application
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
