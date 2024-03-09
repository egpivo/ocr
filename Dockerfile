# Stage 1: Build stage
FROM python:3.12-slim as builder

LABEL maintainer="Joseph Wang <egpivo@gmail.com>" \
      description="Docker image for OCR application" \
      version="0.0.1"

ENV POETRY_HOME=/root/.poetry \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /ocr

RUN apt-get update \
    && apt-get install -y build-essential tesseract-ocr libtesseract-dev \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && poetry config installer.max-workers 10

COPY pyproject.toml poetry.lock ./

# Install dependencies without building
RUN poetry install --no-root

# Copy the rest of the application
COPY . .

# Build the application
RUN poetry build

# Stage 2: Final stage
FROM python:3.12-slim as final

WORKDIR /ocr

# Copy virtual environment, main application files, and distribution files from the builder stage
COPY --from=builder /ocr/.venv ./.venv
COPY --from=builder /ocr/ocr/main.py ./ocr/main.py
COPY --from=builder /ocr/dist/ .

# Install Tesseract and application dependencies
RUN apt-get update \
    && apt-get install -y tesseract-ocr \
    && ./.venv/bin/pip install *.whl

# Entry point to run the application
CMD [".venv/bin/uvicorn", "ocr.main:app", "--host", "0.0.0.0", "--port", "8000"]
