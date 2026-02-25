FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for matplotlib headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY evadex /app/evadex

RUN pip install --upgrade pip && \
    pip install -e .

# Default command shows help
CMD ["evadex-sim", "--help"]

