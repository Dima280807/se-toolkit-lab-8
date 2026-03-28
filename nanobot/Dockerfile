# Multi-stage build for nanobot gateway using uv
# Adapted from backend/Dockerfile pattern

# ---
# Stage 1: Build the application
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB:-}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace and root project files for resolving dependencies
COPY --from=workspace . /app/

# Copy mcp and nanobot-websocket-channel for editable installs
# These come from additional_contexts in docker-compose.yml
COPY --from=mcp . /app/mcp
COPY --from=nanobot-websocket-channel . /app/nanobot-websocket-channel

# Copy nanobot project files (after workspace to avoid overwriting)
COPY . /app/nanobot

# Sync from the root workspace to properly resolve all workspace members
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app && uv sync --package nanobot

# Copy the rest of the nanobot source
COPY . /app/nanobot

# Final sync with all source files (now with mcp and nanobot-websocket-channel available)
RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv sync --package nanobot

# ---
# Stage 2: Runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB:-}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Setup non-root user matching host UID/GID for bind-mount compatibility
# Default is 1000:1000 for typical Linux desktop, but can be overridden
ARG APP_UID=1000
ARG APP_GID=1000
RUN if [ "${APP_UID}" != "0" ]; then \
        groupadd --system --gid ${APP_GID} nonroot \
        && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot; \
    fi

# Copy the application from builder
COPY --from=builder /app /app

# Fix ownership if using non-root user
RUN if [ "${APP_UID}" != "0" ]; then \
        chown -R nonroot:nonroot /app; \
    fi

# Set environment for Python path
ENV PATH="/app/nanobot/.venv/bin:$PATH"

# Switch to non-root user (will be root if APP_UID=0)
ARG APP_UID=1000
ARG APP_GID=1000
USER ${APP_UID}:${APP_GID}

WORKDIR /app/nanobot

# Launch via entrypoint which resolves config and starts gateway
CMD ["python", "/app/nanobot/entrypoint.py"]
