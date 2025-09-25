#!/bin/sh
set -e

until pg_isready -h expenses_postgres -p 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done

alembic upgrade head

# Start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
