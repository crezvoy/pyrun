ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-alpine AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache \
    nsjail \
    py3-pandas \
    py3-numpy

FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY . .

# Does not work on Cloud run
# RUN --mount=type=cache,target=/root/.cache/uv \
#   uv sync --frozen --no-dev

RUN uv sync --frozen --no-dev

FROM base AS runtime
ARG PORT=8080

WORKDIR /app

RUN addgroup --gid 1001 --system apprunner && \
    adduser -H -s /bin/false \
      -D -u 1001 -S -G apprunner apprunner

USER apprunner:apprunner

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PORT=$PORT

COPY --from=builder --chown=apprunner:apprunner /app ./

ENTRYPOINT ["scripts/entrypoint.sh"]
