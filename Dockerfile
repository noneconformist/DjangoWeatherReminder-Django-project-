# Basic image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

LABEL creator="Anton Galkin"

# Turn off interactive
ENV DEBIAN_FRONTEND=noninteractive

# ENV variable to control environment (default prod)
ARG ENV=prod
ENV ENV=${ENV}

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

# Set working directory
WORKDIR /home/docker_user/app

# Copy uv lock file and project configuration
COPY --chown=docker_user:docker_user pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --dev;

ENV PATH="/home/docker_user/app/.venv/bin:$PATH"

# Copying the entire project
COPY --chown=docker_user:docker_user . .

# Fix permissions for docker_user before switching user
RUN chown -R docker_user:docker_user /home/docker_user/app

# Create STATIC_ROOT and grant docker_user permissions
#RUN mkdir -p /home/docker_user/app/staticfiles && \
#    chown -R docker_user:docker_user /home/docker_user/app/staticfiles

# Staticfiles
RUN mkdir -p staticfiles && \
    chown docker_user:docker_user staticfiles

# switch to user
USER docker_user
