#!/bin/sh

set -eu

if [ "${APP_ENV:-prod}" = "dev" ]; then
    echo "Starting server in dev mode with auto-reload"
    exec uvicorn api.main:app \
        --host 0.0.0.0 \
        --port 80 \
        --reload \
        --reload-dir /app/api
else
    echo "Starting server in prod mode"
    exec uvicorn api.main:app --host 0.0.0.0 --port 80
fi
