#!/bin/bash
set -e

echo "Setting up sample database..."

# Wait for PostgreSQL to be ready
until pg_isready -U postgres; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

# Check if database already has tables (already initialized)
TABLE_COUNT=$(psql -U postgres -d sample_db -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null || echo "0")

if [ "$TABLE_COUNT" -gt "0" ]; then
    echo "Database already initialized with $TABLE_COUNT tables. Skipping setup."
else
    echo "Initializing sample database with tables and data..."
    # Run the SQL script to create tables and insert data
    psql -U postgres -d sample_db -f /docker-entrypoint-initdb.d/init-sample-db.sql
    
    # Verify setup
    TABLE_COUNT_AFTER=$(psql -U postgres -d sample_db -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null || echo "0")
    if [ "$TABLE_COUNT_AFTER" -gt "0" ]; then
        echo "✅ Sample database initialized successfully with $TABLE_COUNT_AFTER tables!"
    else
        echo "⚠️  Warning: Database initialization may have failed."
    fi
fi

