#!/bin/sh
set -e

BACKUP_FILE="/docker-entrypoint-initdb.d/formulacion_magistral_db"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup not found: $BACKUP_FILE" >&2
    exit 1
fi

echo "Restoring PostgreSQL backup into ${POSTGRES_DB}..."
pg_restore --no-owner --no-acl --role="$POSTGRES_USER" --dbname="$POSTGRES_DB" "$BACKUP_FILE"
