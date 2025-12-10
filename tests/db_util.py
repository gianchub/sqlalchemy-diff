"""Database utility functions for PostgreSQL and SQLite.

These functions replace sqlalchemy-utils functionality for test purposes.
"""

from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import create_engine, text


def _parse_database_uri(uri):
    """Parse a database URI and return components."""
    parsed = urlparse(uri)
    return {
        "scheme": parsed.scheme,
        "username": parsed.username,
        "password": parsed.password,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "database": parsed.path.lstrip("/") if parsed.path else None,
        "path": parsed.path,
    }


def _get_postgres_admin_uri(uri):
    """Get a PostgreSQL URI pointing to the 'postgres' database for admin operations."""
    parsed = _parse_database_uri(uri)
    # Connect to 'postgres' database instead of the target database
    admin_uri = (
        f"postgresql://{parsed['username']}:{parsed['password']}@"
        f"{parsed['hostname']}:{parsed['port']}/postgres"
    )
    return admin_uri


def _get_sqlite_file_path(uri):
    """Extract the file path from a SQLite URI as a Path object."""
    parsed = _parse_database_uri(uri)
    path = parsed["path"]

    # Handle :memory: and empty path
    if not path or path == "/:memory:":
        return None

    # Remove leading slash
    if path.startswith("/"):
        path = path[1:]

    return Path(path)


def database_exists(uri):
    """Check if a database exists.

    Args:
        uri: Database URI (postgresql://... or sqlite:///...)

    Returns:
        bool: True if database exists, False otherwise
    """
    parsed = _parse_database_uri(uri)
    scheme = parsed["scheme"]

    if scheme == "postgresql":
        admin_uri = _get_postgres_admin_uri(uri)
        target_db = parsed["database"]

        engine = create_engine(admin_uri, isolation_level="AUTOCOMMIT")
        try:
            with engine.connect() as conn:
                result = conn.execute(
                    text(
                        "SELECT 1 FROM pg_database WHERE datname = :dbname"
                    ),
                    {"dbname": target_db}
                )
                return result.fetchone() is not None
        finally:
            engine.dispose()

    elif scheme == "sqlite":
        file_path = _get_sqlite_file_path(uri)

        # In-memory databases always "exist" (they're created on connection)
        if file_path is None:
            return True

        # For file-based SQLite, check if file exists
        return file_path.exists()

    else:
        raise ValueError(f"Unsupported database scheme: {scheme}")


def create_database(uri):
    """Create a database.

    Args:
        uri: Database URI (postgresql://... or sqlite:///...)
    """
    parsed = _parse_database_uri(uri)
    scheme = parsed["scheme"]

    if scheme == "postgresql":
        admin_uri = _get_postgres_admin_uri(uri)
        target_db = parsed["database"]

        engine = create_engine(admin_uri, isolation_level="AUTOCOMMIT")
        try:
            with engine.connect() as conn:
                # Database should not exist since create_db() calls drop_db() first
                conn.execute(text(f'CREATE DATABASE "{target_db}"'))
        finally:
            engine.dispose()

    elif scheme == "sqlite":
        file_path = _get_sqlite_file_path(uri)

        # In-memory databases don't need creation
        if file_path is None:
            return

        # For file-based SQLite, ensure the directory exists
        if file_path.parent:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create an empty file to "create" the database
        # SQLite will create the file on first connection, but we'll touch it here
        if not file_path.exists():
            file_path.touch()

    else:
        raise ValueError(f"Unsupported database scheme: {scheme}")


def drop_database(uri):
    """Drop a database.

    Args:
        uri: Database URI (postgresql://... or sqlite:///...)
    """
    parsed = _parse_database_uri(uri)
    scheme = parsed["scheme"]

    if scheme == "postgresql":
        admin_uri = _get_postgres_admin_uri(uri)
        target_db = parsed["database"]

        engine = create_engine(admin_uri, isolation_level="AUTOCOMMIT")
        try:
            with engine.connect() as conn:
                # Terminate any existing connections to the database
                conn.execute(
                    text(
                        """
                        SELECT pg_terminate_backend(pg_stat_activity.pid)
                        FROM pg_stat_activity
                        WHERE pg_stat_activity.datname = :dbname
                        AND pid <> pg_backend_pid()
                        """
                    ),
                    {"dbname": target_db}
                )
                # Drop the database
                conn.execute(text(f'DROP DATABASE IF EXISTS "{target_db}"'))
        finally:
            engine.dispose()

    elif scheme == "sqlite":
        file_path = _get_sqlite_file_path(uri)

        # In-memory databases don't need dropping
        if file_path is None:
            return

        # For file-based SQLite, delete the file
        if file_path.exists():
            file_path.unlink()

    else:
        raise ValueError(f"Unsupported database scheme: {scheme}")

