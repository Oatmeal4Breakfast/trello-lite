FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy only Poetry files first (for caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies (app + dev tools)
RUN poetry install --no-root --no-interaction --no-ansi
# Copy only source code (not the .venv folder)
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Run Uvicorn via Poetry
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
