FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY . .

ARG COMMIT=unknown
ARG COMMIT_FULL=unknown
ENV COMMIT=$COMMIT
ENV COMMIT_FULL=$COMMIT_FULL

RUN python build.py
