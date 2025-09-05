# Base image with Python 3.12 and uv preinstalled
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Ensure uv is always available
ENV PATH="/usr/local/bin:/app/.venv/bin:$PATH"

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Copy dependency files only (better for Docker caching)
COPY pyproject.toml uv.lock ./

# Install project dependencies (but not the app yet)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Copy application code
COPY app ./app

# Sync project itself into the venv
RUN uv sync --locked

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI using uv + uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
