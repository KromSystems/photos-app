# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Set workdir for all stages
WORKDIR /app

FROM base AS builder

# Install build dependencies (for Pillow, psycopg2)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install dependencies
RUN python -m venv .venv

# Install Python dependencies using pip cache and bind mount for requirements.txt
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt,readonly \
    --mount=type=cache,target=/root/.cache/pip \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Copy application source code (excluding .env and venv)
COPY --link app.py config.py db.py ./

FROM base AS final

# Create non-root user
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source code from builder
COPY --from=builder /app/app.py /app/config.py /app/db.py ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Set permissions
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
