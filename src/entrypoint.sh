#!/bin/sh

LOWER_LOG_LEVEL=$(echo "$LOG_LEVEL" | tr '[:upper:]' '[:lower:]')

exec uvicorn app:app \
  --host $HOST \
  --port $PORT \
  --workers $UVICORN_WORKERS \
  --log-level $LOWER_LOG_LEVEL
