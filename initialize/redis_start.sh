#!/bin/sh
set -e

# Run Redis with append-only persistence enabled and password
exec redis-server --appendonly yes --requirepass "${REDIS_PASSWORD}"
