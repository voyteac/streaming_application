#!/bin/bash

DB_NAME="streaming_app"
TABLE_NAME="data_ingress_databaseloader"
USER="myuser"
HOST="localhost"
PGPASSWORD="mypassword"

export PGPASSWORD

psql -U "$USER" -h "$HOST" -p "$PORT" -d "$DB_NAME" -c "DELETE FROM \"$TABLE_NAME\";"

unset PGPASSWORD

if [ $? -eq 0 ]; then
    echo "Table $TABLE_NAME has been successfully truncated."
else
    echo "Failed to truncate table $TABLE_NAME."
fi
