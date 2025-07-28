#!/bin/sh
set -e

echo "Executing alembic migrations"
alembic upgrade head

echo "Starting Fastapi App with Uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000