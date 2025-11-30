"""Configuration management for database connection."""

import os
import sys

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from sqlalchemy.exc import ProgrammingError, OperationalError

# Load environment variables from .env
load_dotenv()

# Default local PostgreSQL database (Docker container)
# This provides a working database out of the box, similar to Chinook.db for SQLite
# Start with: docker-compose up -d
DEFAULT_POSTGRES_URI = (
    "postgresql://postgres:postgres@localhost:5432/sample_db"
)


def get_database_uri() -> str:
    """
    Get PostgreSQL URI with fallback to default.

    Priority:
    1. POSTGRES_URI env var (if provided)
    2. Default public PostgreSQL database
    """
    uri = os.getenv("POSTGRES_URI")
    if uri:
        return uri
    return DEFAULT_POSTGRES_URI


def get_database() -> SQLDatabase:
    """
    Get SQLDatabase instance for PostgreSQL.
    
    Raises:
        SystemExit: If database connection fails with a user-friendly error message.
    """
    uri = get_database_uri()
    
    try:
        # Try to create database connection with schema reflection
        # Some databases may have limited permissions, so we'll handle that gracefully
        return SQLDatabase.from_uri(uri)
    except (ProgrammingError, OperationalError) as e:
        # Connection or permission error
        error_msg = str(e)
        
        # Provide user-friendly error message
        print("\n" + "=" * 60, file=sys.stderr)
        print("❌ Database Connection Error", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("\nThere was a problem connecting to the PostgreSQL database.", file=sys.stderr)
        print("\nPossible causes:", file=sys.stderr)
        print("  • Database server is not accessible", file=sys.stderr)
        print("  • Insufficient permissions for schema reflection", file=sys.stderr)
        print("  • Invalid connection string", file=sys.stderr)
        print("\nTo fix:", file=sys.stderr)
        print("  1. Start the default database: docker-compose up -d", file=sys.stderr)
        print("  2. Or set POSTGRES_URI in your .env file with your own database", file=sys.stderr)
        print(f"\nConnection URI: {uri.split('@')[1] if '@' in uri else 'hidden'}", file=sys.stderr)
        print(f"\nTechnical error: {error_msg[:200]}...", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Other unexpected errors
        print("\n" + "=" * 60, file=sys.stderr)
        print("❌ Unexpected Database Error", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"\nAn unexpected error occurred while connecting to the database:", file=sys.stderr)
        print(f"{type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
        print("\nPlease check your database connection settings.", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)

