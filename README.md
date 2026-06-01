# ml-api

## Run modes

Server mode is controlled through `.env`.

Example:

```env
APP_ENV=dev
APP_PORT=8000
API_TOKEN=your-token
LOKI_PORT=3100
GRAFANA_PORT=3000
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

Values:

- `APP_ENV=dev` - starts `uvicorn` with `--reload`, and code changes in `api/` are applied automatically.
- `APP_ENV=prod` - starts the server without auto-reload.

## Logging

The Docker stack includes `Loki`, `Grafana`, and `Alloy`.

- `Alloy` reads container logs from Docker and ships them to `Loki`.
- `Grafana` is provisioned with `Loki` as the default datasource.
- `Grafana` preinstalls the `grafana-lokiexplore-app` plugin required for `Logs Drilldown`.
- Application logs already go to `stdout`, so `api` and `iris` logs appear in `Loki` automatically.
- Loki is configured with `volume_enabled: true`, which is required for Grafana `Logs Drilldown`.

After startup:

- Grafana: `http://localhost:${GRAFANA_PORT}`
- Loki: `http://localhost:${LOKI_PORT}`

Open Grafana and query logs by labels such as `service`, `container`, and `stream`.
In `Logs Drilldown`, logs should appear grouped by `service_name` for each Compose service/container.
