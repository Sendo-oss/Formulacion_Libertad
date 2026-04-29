#!/bin/sh
set -e

python - <<'PY'
import os
import socket
import time

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))
deadline = time.time() + 60

while True:
    try:
        with socket.create_connection((host, port), timeout=3):
            break
    except OSError:
        if time.time() > deadline:
            raise SystemExit(f"Database is not reachable at {host}:{port}")
        time.sleep(2)
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
