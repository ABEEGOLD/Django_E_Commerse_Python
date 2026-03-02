# Use Python 3.14 slim
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# ---------------------------
# Install system dependencies for mysqlclient & build tools
# ---------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install uv package manager
# ---------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# ---------------------------
# Copy project files (code only, .venv is not copied/mounted in dev)
# ---------------------------
COPY . .

# ---------------------------
# Install Python dependencies
# ---------------------------
RUN uv sync --no-cache --refresh

# ---------------------------
# Create empty folders for container static files and venv
# Prevent overwriting local .venv & static files when mounted
# ---------------------------
RUN mkdir -p /app/.venv /app/staticfiles

# ---------------------------
# Expose Django dev port
# ---------------------------
EXPOSE 8000

# ---------------------------
# Environment variables for development
# ---------------------------
ENV DJANGO_ENV=development
ENV ENV_FILE=.env.local

# ---------------------------
# Command for local development with live reload
# ---------------------------
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]