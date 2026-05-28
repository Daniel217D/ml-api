#!/bin/sh

set -eu

ENV_FILE="/app/.env"

if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
fi

current_token="$(sed -n 's/^API_TOKEN=//p' "$ENV_FILE" | tail -n 1 | tr -d '"' | tr -d "'" | tr -d '[:space:]')"

if [ -z "$current_token" ]; then
    generated_token="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

    if grep -q '^API_TOKEN=' "$ENV_FILE"; then
        temp_file="$(mktemp)"
        sed "s|^API_TOKEN=.*|API_TOKEN=$generated_token|" "$ENV_FILE" > "$temp_file"
        cat "$temp_file" > "$ENV_FILE"
        rm -f "$temp_file"
    else
        printf '\nAPI_TOKEN=%s\n' "$generated_token" >> "$ENV_FILE"
    fi

    echo "Generated API_TOKEN and saved it to $ENV_FILE"
fi

set -a
. "$ENV_FILE"
set +a

APP_ENV="${APP_ENV:-prod}"

if [ "$APP_ENV" = "dev" ]; then
    echo "Starting server in dev mode with auto-reload"
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 80 \
        --reload \
        --reload-dir /app/app
fi

echo "Starting server in prod mode"
exec uvicorn app.main:app --host 0.0.0.0 --port 80
