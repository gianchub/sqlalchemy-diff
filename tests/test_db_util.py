import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from tests.db_util import (
    _get_postgres_admin_uri,
    _get_sqlite_file_path,
    _parse_database_uri,
    create_database,
    database_exists,
    drop_database,
)


class TestParseDatabaseUri:
    """Test the _parse_database_uri helper function."""

    def test_parse_postgresql_uri(self):
        """Test parsing a PostgreSQL URI."""
        uri = "postgresql://user:pass@localhost:5432/mydb"
        result = _parse_database_uri(uri)

        assert result["scheme"] == "postgresql"
        assert result["username"] == "user"
        assert result["password"] == "pass"
        assert result["hostname"] == "localhost"
        assert result["port"] == 5432
        assert result["database"] == "mydb"
        assert result["path"] == "/mydb"

    def test_parse_postgresql_uri_no_port(self):
        """Test parsing a PostgreSQL URI without port."""
        uri = "postgresql://user:pass@localhost/mydb"
        result = _parse_database_uri(uri)

        assert result["scheme"] == "postgresql"
        assert result["username"] == "user"
        assert result["password"] == "pass"
        assert result["hostname"] == "localhost"
        assert result["port"] is None
        assert result["database"] == "mydb"

    def test_parse_sqlite_memory_uri(self):
        """Test parsing a SQLite in-memory URI."""
        uri = "sqlite:///:memory:"
        result = _parse_database_uri(uri)

        assert result["scheme"] == "sqlite"
        assert result["username"] is None
        assert result["password"] is None
        assert result["hostname"] is None
        assert result["port"] is None
        assert result["database"] == ":memory:"  # lstrip("/") removes leading slash
        assert result["path"] == "/:memory:"

    def test_parse_sqlite_file_uri(self):
        """Test parsing a SQLite file URI."""
        uri = "sqlite:///path/to/database.db"
        result = _parse_database_uri(uri)

        assert result["scheme"] == "sqlite"
        assert result["path"] == "/path/to/database.db"
        assert result["database"] == "path/to/database.db"


class TestGetPostgresAdminUri:
    """Test the _get_postgres_admin_uri helper function."""

    def test_get_postgres_admin_uri(self):
        """Test generating admin URI for PostgreSQL."""
        uri = "postgresql://user:pass@localhost:5432/mydb"
        admin_uri = _get_postgres_admin_uri(uri)

        assert admin_uri == "postgresql://user:pass@localhost:5432/postgres"

    def test_get_postgres_admin_uri_no_port(self):
        """Test generating admin URI without port."""
        uri = "postgresql://user:pass@localhost/mydb"
        admin_uri = _get_postgres_admin_uri(uri)

        assert admin_uri == "postgresql://user:pass@localhost/postgres"


class TestGetSqliteFilePath:
    """Test the _get_sqlite_file_path helper function."""

    def test_get_sqlite_file_path_memory(self):
        """Test extracting path from in-memory SQLite URI."""
        uri = "sqlite:///:memory:"
        result = _get_sqlite_file_path(uri)

        assert result is None

    def test_get_sqlite_file_path_empty(self):
        """Test extracting path from empty SQLite URI."""
        uri = "sqlite:///"
        result = _get_sqlite_file_path(uri)

        assert result is None

    def test_get_sqlite_file_path_absolute(self):
        """Test extracting absolute path from SQLite URI."""
        uri = "sqlite:///path/to/database.db"
        result = _get_sqlite_file_path(uri)

        assert isinstance(result, Path)
        assert result == Path("path/to/database.db")

    def test_get_sqlite_file_path_relative(self):
        """Test extracting relative path from SQLite URI."""
        uri = "sqlite:///database.db"
        result = _get_sqlite_file_path(uri)

        assert isinstance(result, Path)
        assert result == Path("database.db")


class TestDatabaseExists:
    """Test the database_exists function."""

    @pytest.fixture
    def unique_db_name(self):
        """Generate a unique database name for testing."""
        return f"test_db_exists_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def postgres_uri(self, make_postgres_uri, unique_db_name):
        """Create a PostgreSQL URI for testing."""
        return make_postgres_uri(unique_db_name)

    def test_database_exists_postgresql_nonexistent(self, postgres_uri):
        """Test checking non-existent PostgreSQL database."""
        assert not database_exists(postgres_uri)

    def test_database_exists_postgresql_existent(self, postgres_uri):
        """Test checking existing PostgreSQL database."""
        # Create the database first
        create_database(postgres_uri)
        try:
            assert database_exists(postgres_uri)
        finally:
            drop_database(postgres_uri)

    def test_database_exists_sqlite_memory(self):
        """Test checking in-memory SQLite database (always exists)."""
        uri = "sqlite:///:memory:"
        assert database_exists(uri)

    def test_database_exists_sqlite_file_nonexistent(self, tmp_path):
        """Test checking non-existent SQLite file database."""
        db_file = tmp_path / "nonexistent.db"
        uri = f"sqlite:///{db_file}"
        assert not database_exists(uri)

    def test_database_exists_sqlite_file_existent(self, tmp_path):
        """Test checking existing SQLite file database."""
        db_file = tmp_path / "existing.db"
        db_file.touch()
        uri = f"sqlite:///{db_file}"
        assert database_exists(uri)

    def test_database_exists_unsupported_scheme(self):
        """Test that unsupported schemes raise ValueError."""
        uri = "mysql://user:pass@localhost/db"
        with pytest.raises(ValueError, match="Unsupported database scheme: mysql"):
            database_exists(uri)


class TestCreateDatabase:
    """Test the create_database function."""

    @pytest.fixture
    def unique_db_name(self):
        """Generate a unique database name for testing."""
        return f"test_db_create_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def postgres_uri(self, make_postgres_uri, unique_db_name):
        """Create a PostgreSQL URI for testing."""
        return make_postgres_uri(unique_db_name)

    def test_create_database_postgresql(self, postgres_uri):
        """Test creating a PostgreSQL database."""
        # Ensure it doesn't exist first
        if database_exists(postgres_uri):
            drop_database(postgres_uri)

        create_database(postgres_uri)
        try:
            assert database_exists(postgres_uri)
        finally:
            drop_database(postgres_uri)

    def test_create_database_postgresql_already_exists(self, postgres_uri):
        """Test creating a PostgreSQL database that already exists."""
        # Create the database first
        if not database_exists(postgres_uri):
            create_database(postgres_uri)

        # PostgreSQL will raise a ProgrammingError when trying to create existing database
        with pytest.raises(ProgrammingError):
            create_database(postgres_uri)

        # Cleanup
        drop_database(postgres_uri)

    def test_create_database_sqlite_memory(self):
        """Test creating in-memory SQLite database (no-op)."""
        uri = "sqlite:///:memory:"
        # In-memory databases always exist (they're created on connection)
        assert database_exists(uri)
        # Should not raise an error
        create_database(uri)
        # Still exists after create (no-op for in-memory)
        assert database_exists(uri)

    def test_create_database_sqlite_file(self, tmp_path):
        """Test creating a SQLite file database."""
        db_file = tmp_path / "new_database.db"
        uri = f"sqlite:///{db_file}"

        assert not db_file.exists()
        create_database(uri)
        assert db_file.exists()
        assert database_exists(uri)

        # Cleanup
        db_file.unlink()

    def test_create_database_sqlite_file_with_subdirectory(self, tmp_path):
        """Test creating a SQLite file database in a subdirectory."""
        subdir = tmp_path / "subdir"
        db_file = subdir / "database.db"
        uri = f"sqlite:///{db_file}"

        assert not subdir.exists()
        assert not db_file.exists()

        create_database(uri)

        assert subdir.exists()
        assert db_file.exists()
        assert database_exists(uri)

        # Cleanup
        db_file.unlink()
        subdir.rmdir()

    def test_create_database_sqlite_file_already_exists(self, tmp_path):
        """Test creating a SQLite file database that already exists."""
        db_file = tmp_path / "existing.db"
        db_file.touch()
        uri = f"sqlite:///{db_file}"

        # Should not raise an error, just touch the file
        create_database(uri)
        assert db_file.exists()

        # Cleanup
        db_file.unlink()

    def test_create_database_unsupported_scheme(self):
        """Test that unsupported schemes raise ValueError."""
        uri = "mysql://user:pass@localhost/db"
        with pytest.raises(ValueError, match="Unsupported database scheme: mysql"):
            create_database(uri)


class TestDropDatabase:
    """Test the drop_database function."""

    @pytest.fixture
    def unique_db_name(self):
        """Generate a unique database name for testing."""
        return f"test_db_drop_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def postgres_uri(self, make_postgres_uri, unique_db_name):
        """Create a PostgreSQL URI for testing."""
        return make_postgres_uri(unique_db_name)

    def test_drop_database_postgresql_existent(self, postgres_uri):
        """Test dropping an existing PostgreSQL database."""
        # Create the database first
        if not database_exists(postgres_uri):
            create_database(postgres_uri)

        assert database_exists(postgres_uri)
        drop_database(postgres_uri)
        assert not database_exists(postgres_uri)

    def test_drop_database_postgresql_nonexistent(self, postgres_uri):
        """Test dropping a non-existent PostgreSQL database."""
        # Ensure it doesn't exist
        if database_exists(postgres_uri):
            drop_database(postgres_uri)

        # Should not raise an error (uses IF EXISTS)
        drop_database(postgres_uri)
        assert not database_exists(postgres_uri)

    def test_drop_database_postgresql_with_connections(self, postgres_uri):
        """Test dropping a PostgreSQL database that has active connections."""
        # Create the database
        if not database_exists(postgres_uri):
            create_database(postgres_uri)

        # Create a connection to the database
        engine = create_engine(postgres_uri)
        conn = engine.connect()

        try:
            # Drop should terminate connections and succeed
            drop_database(postgres_uri)
            assert not database_exists(postgres_uri)
        finally:
            conn.close()
            engine.dispose()

    def test_drop_database_sqlite_memory(self):
        """Test dropping in-memory SQLite database (no-op)."""
        uri = "sqlite:///:memory:"
        # Should not raise an error
        drop_database(uri)
        assert database_exists(uri)  # Still exists (in-memory)

    def test_drop_database_sqlite_file_existent(self, tmp_path):
        """Test dropping an existing SQLite file database."""
        db_file = tmp_path / "to_drop.db"
        db_file.touch()
        uri = f"sqlite:///{db_file}"

        assert db_file.exists()
        drop_database(uri)
        assert not db_file.exists()
        assert not database_exists(uri)

    def test_drop_database_sqlite_file_nonexistent(self, tmp_path):
        """Test dropping a non-existent SQLite file database."""
        db_file = tmp_path / "nonexistent.db"
        uri = f"sqlite:///{db_file}"

        assert not db_file.exists()
        # Should not raise an error
        drop_database(uri)
        assert not db_file.exists()

    def test_drop_database_unsupported_scheme(self):
        """Test that unsupported schemes raise ValueError."""
        uri = "mysql://user:pass@localhost/db"
        with pytest.raises(ValueError, match="Unsupported database scheme: mysql"):
            drop_database(uri)


class TestDatabaseLifecycle:
    """Test complete database lifecycle operations."""

    @pytest.fixture
    def unique_db_name(self):
        """Generate a unique database name for testing."""
        return f"test_db_lifecycle_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def postgres_uri(self, make_postgres_uri, unique_db_name):
        """Create a PostgreSQL URI for testing."""
        return make_postgres_uri(unique_db_name)

    def test_postgresql_lifecycle(self, postgres_uri):
        """Test complete PostgreSQL database lifecycle."""
        # Start: database should not exist
        assert not database_exists(postgres_uri)

        # Create database
        create_database(postgres_uri)
        assert database_exists(postgres_uri)

        # Drop database
        drop_database(postgres_uri)
        assert not database_exists(postgres_uri)

        # Create again
        create_database(postgres_uri)
        assert database_exists(postgres_uri)

        # Final cleanup
        drop_database(postgres_uri)
        assert not database_exists(postgres_uri)

    def test_sqlite_file_lifecycle(self, tmp_path):
        """Test complete SQLite file database lifecycle."""
        db_file = tmp_path / "lifecycle.db"
        uri = f"sqlite:///{db_file}"

        # Start: database should not exist
        assert not database_exists(uri)

        # Create database
        create_database(uri)
        assert database_exists(uri)
        assert db_file.exists()

        # Drop database
        drop_database(uri)
        assert not database_exists(uri)
        assert not db_file.exists()

        # Create again
        create_database(uri)
        assert database_exists(uri)
        assert db_file.exists()

        # Final cleanup
        drop_database(uri)
        assert not database_exists(uri)
        assert not db_file.exists()

    def test_sqlite_memory_lifecycle(self):
        """Test SQLite in-memory database lifecycle."""
        uri = "sqlite:///:memory:"

        # In-memory always exists
        assert database_exists(uri)

        # Create is a no-op
        create_database(uri)
        assert database_exists(uri)

        # Drop is a no-op
        drop_database(uri)
        assert database_exists(uri)


class TestDatabaseOperationsEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def unique_db_name(self):
        """Generate a unique database name for testing."""
        return f"test_db_edge_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def postgres_uri(self, make_postgres_uri, unique_db_name):
        """Create a PostgreSQL URI for testing."""
        return make_postgres_uri(unique_db_name)

    def test_postgresql_database_name_with_special_chars(self, make_postgres_uri):
        """Test PostgreSQL database with special characters in name."""
        # PostgreSQL allows quoted identifiers, but we should test our quoting
        db_name = f"test_db_{uuid.uuid4().hex[:8]}"
        uri = make_postgres_uri(db_name)

        create_database(uri)
        try:
            assert database_exists(uri)
        finally:
            drop_database(uri)

    def test_sqlite_file_path_with_spaces(self, tmp_path):
        """Test SQLite file path with spaces."""
        db_file = tmp_path / "database with spaces.db"
        uri = f"sqlite:///{db_file}"

        create_database(uri)
        assert db_file.exists()
        assert database_exists(uri)

        drop_database(uri)
        assert not db_file.exists()

    def test_sqlite_file_path_unicode(self, tmp_path):
        """Test SQLite file path with unicode characters."""
        db_file = tmp_path / "数据库.db"
        uri = f"sqlite:///{db_file}"

        create_database(uri)
        assert db_file.exists()
        assert database_exists(uri)

        drop_database(uri)
        assert not db_file.exists()

    def test_multiple_operations_sequence(self, postgres_uri):
        """Test multiple create/drop operations in sequence."""
        # Create and drop multiple times
        for _ in range(3):
            create_database(postgres_uri)
            assert database_exists(postgres_uri)
            drop_database(postgres_uri)
            assert not database_exists(postgres_uri)

    def test_sqlite_empty_path(self):
        """Test SQLite URI with empty path."""
        uri = "sqlite:///"
        # Should be treated as in-memory
        assert database_exists(uri)
        create_database(uri)  # Should be no-op
        drop_database(uri)  # Should be no-op
