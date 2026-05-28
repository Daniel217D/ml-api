# ml-api

## Run modes

Server mode is controlled through `.env`.

Example:

```env
APP_ENV=dev
APP_PORT=8000
API_TOKEN=your-token
```

Values:

- `APP_ENV=dev` - starts `uvicorn` with `--reload`, and code changes in `app/` are applied automatically.
- `APP_ENV=prod` - starts the server without auto-reload.
