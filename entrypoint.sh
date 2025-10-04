#!/bin/bash
set -e

# Wait for Postgres
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Wait for Redis
until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" ping; do
  >&2 echo "Redis is unavailable - sleeping"
  sleep 1
done

# Run migrations
alembic upgrade head

# Start Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4