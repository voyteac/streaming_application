#!/bin/bash


DB_NAME="streaming_app"
TABLE_NAME="data_ingress_databaseloader"
USER="myuser"
HOST="localhost"
PGPASSWORD="mypassword"

export PGPASSWORD

COLUMN1="internal_unique_client_id"
COLUMN2="unique_client_id"
COLUMN3="timestamp"
COLUMN4="message_number"
COLUMN5="client_name"

echo "Displaying table $TABLE_NAME content:"
psql -U "$USER" -h "$HOST" -p "$PORT" -d "$DB_NAME" -c "SELECT \"$COLUMN1\", \"$COLUMN2\", \"$COLUMN3\", \"$COLUMN4\", \"$COLUMN5\" FROM \"$TABLE_NAME\";"

unset PGPASSWORD


