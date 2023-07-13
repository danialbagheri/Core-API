#!/bin/bash

# Set the PostgreSQL username and database name
PG_USER=your_username
PG_DB=your_database_name
CONTAINER_NAME=your_container_name
BRAND_NAME=your_brand_name

# Set the backup directory and filename
BACKUP_DIR=/var/backups/${BRAND_NAME}/postgres
BACKUP_FILE=pg_backup_$(date +%Y-%m-%dT%H:%M:%S).sql

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Use pg_dump to create the backup file
docker exec -it "$CONTAINER_NAME" pg_dump -U "$PG_USER" "$PG_DB" > "$BACKUP_DIR"/"$BACKUP_FILE"

# Set the file permissions to only be readable by root
chmod 600 "$BACKUP_DIR"/"$BACKUP_FILE"

# Delete backups older than 24 hours
find "$BACKUP_DIR" -name "*.sql" -mtime +1 -exec rm {} \;