"""
Tests for database engine support.

Tests database drivers, integration with open_iterable(), convert(), and pipeline().
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from iterable.db import get_driver, is_database_engine, list_drivers, register_driver
from iterable.db.base import DBDriver
from iterable.db.iterable import DatabaseIterable
from iterable.db.postgres import PostgresDriver


class TestPostgresDriver:
    """Test PostgreSQL driver implementation."""

    def test_connect_with_connection_string(self):
        """Test connection with connection string."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

            driver = PostgresDriver("postgresql://user:pass@localhost/db", query="SELECT 1")
            driver.connect()

            assert driver.is_connected
            assert driver.conn == mock_conn
            mock_psycopg2.connect.assert_called_once_with("postgresql://user:pass@localhost/db", **{})

    def test_connect_with_existing_connection(self):
        """Test connection with existing connection object."""
        mock_conn = MagicMock()
        mock_conn.cursor = MagicMock()
        mock_conn.close = MagicMock()

        driver = PostgresDriver(mock_conn, query="SELECT 1")
        driver.connect()

        assert driver.is_connected
        assert driver.conn == mock_conn

    def test_connect_import_error(self):
        """Test ImportError when psycopg2 not installed."""
        with patch.dict("sys.modules", {"psycopg2": None}):
            # Force reimport to trigger ImportError
            import sys

            if "iterable.db.postgres" in sys.modules:
                del sys.modules["iterable.db.postgres"]

            from iterable.db.postgres import PostgresDriver

            driver = PostgresDriver("postgresql://localhost/db", query="SELECT 1")
            with pytest.raises(ImportError, match="psycopg2-binary is required"):
                driver.connect()

    def test_connect_with_connect_args(self):
        """Test connection with additional connect_args."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

            driver = PostgresDriver(
                "postgresql://localhost/db",
                query="SELECT 1",
                connect_args={"sslmode": "require"},
            )
            driver.connect()

            mock_psycopg2.connect.assert_called_once_with("postgresql://localhost/db", sslmode="require")

    def test_read_only_transaction(self):
        """Test read-only transaction is set."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="SELECT 1", read_only=True)
            driver.connect()

            mock_conn.set_isolation_level.assert_called_once_with(ISOLATION_LEVEL_READ_COMMITTED)
            mock_conn.cursor.assert_called()
            mock_conn.commit.assert_called_once()

    def test_build_query_from_table_name(self):
        """Test auto-building SELECT query from table name."""
        driver = PostgresDriver("postgresql://localhost/db", query="users")
        query = driver._build_query()
        assert query == 'SELECT * FROM "users"'

    def test_build_query_with_schema(self):
        """Test query building with schema."""
        driver = PostgresDriver("postgresql://localhost/db", query="users", schema="public")
        query = driver._build_query()
        assert query == '"public"."users"'

    def test_build_query_with_columns(self):
        """Test query building with column projection."""
        driver = PostgresDriver("postgresql://localhost/db", query="users", columns=["id", "name"])
        query = driver._build_query()
        assert '"id"' in query
        assert '"name"' in query
        assert "*" not in query

    def test_build_query_with_filter(self):
        """Test query building with WHERE clause."""
        driver = PostgresDriver("postgresql://localhost/db", query="users", filter="active = TRUE")
        query = driver._build_query()
        assert "WHERE active = TRUE" in query

    def test_build_query_with_sql_string(self):
        """Test query building with SQL string."""
        sql = "SELECT id, name FROM users WHERE age > 18"
        driver = PostgresDriver("postgresql://localhost/db", query=sql)
        query = driver._build_query()
        assert query == sql

    def test_quote_identifier(self):
        """Test identifier quoting."""
        driver = PostgresDriver("postgresql://localhost/db", query="test")
        assert driver._quote_identifier("user") == '"user"'
        assert driver._quote_identifier('user"name') == '"user""name"'

    def test_iterate_with_server_side_cursor(self):
        """Test streaming iteration with server-side cursor."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.description = [("id",), ("name",)]
            mock_cursor.fetchmany.side_effect = [
                [(1, "Alice"), (2, "Bob")],
                [],
            ]
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="users", batch_size=2)
            driver.connect()

            rows = list(driver.iterate())
            assert len(rows) == 2
            assert rows[0] == {"id": 1, "name": "Alice"}
            assert rows[1] == {"id": 2, "name": "Bob"}
            assert mock_cursor.itersize == 2
            mock_cursor.execute.assert_called_once()

    def test_iterate_with_regular_cursor(self):
        """Test iteration with regular cursor (no server-side)."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.description = [("id",), ("name",)]
            mock_cursor.__iter__.return_value = iter([(1, "Alice"), (2, "Bob")])
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="users", server_side_cursor=False)
            driver.connect()

            rows = list(driver.iterate())
            assert len(rows) == 2
            assert rows[0] == {"id": 1, "name": "Alice"}
            assert rows[1] == {"id": 2, "name": "Bob"}

    def test_iterate_empty_result_set(self):
        """Test iteration with empty result set."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.description = [("id",)]
            mock_cursor.fetchmany.return_value = []
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="users")
            driver.connect()

            rows = list(driver.iterate())
            assert len(rows) == 0

    def test_iterate_no_columns(self):
        """Test iteration with no column description."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.description = None
            mock_cursor.fetchmany.return_value = [()]
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="INSERT INTO users VALUES (1)")
            driver.connect()

            rows = list(driver.iterate())
            assert len(rows) == 1
            assert rows[0] == {}

    def test_metrics_tracking(self):
        """Test metrics are tracked during iteration."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.description = [("id",)]
            mock_cursor.fetchmany.side_effect = [
                [(1,), (2,), (3,)],
                [],
            ]
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="users")
            driver.connect()

            list(driver.iterate())
            metrics = driver.metrics
            assert metrics["rows_read"] == 3
            assert metrics["elapsed_seconds"] >= 0

    def test_list_tables(self):
        """Test list_tables() helper function."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                ("public", "users", 1000),
                ("public", "orders", 500),
            ]
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

            tables = PostgresDriver.list_tables("postgresql://localhost/db")
            assert len(tables) == 2
            assert tables[0]["schema"] == "public"
            assert tables[0]["table"] == "users"
            assert tables[0]["row_count"] == 1000

    def test_list_tables_with_schema(self):
        """Test list_tables() with schema filter."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [("test", "users", 100)]
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

            tables = PostgresDriver.list_tables("postgresql://localhost/db", schema="test")
            assert len(tables) == 1
            assert tables[0]["schema"] == "test"

    def test_error_handling_raise(self):
        """Test error handling with 'raise' policy."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.execute.side_effect = Exception("SQL error")
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="INVALID SQL", on_error="raise")
            driver.connect()

            with pytest.raises(Exception, match="SQL error"):
                list(driver.iterate())

    def test_error_handling_skip(self):
        """Test error handling with 'skip' policy."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.execute.side_effect = Exception("SQL error")
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="INVALID SQL", on_error="skip")
            driver.connect()

            rows = list(driver.iterate())
            assert len(rows) == 0  # Error skipped, no rows returned

    def test_close_cleans_up_cursor(self):
        """Test close() cleans up cursor."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="users")
            driver.connect()
            driver._cursor = mock_cursor
            driver.close()

            mock_cursor.close.assert_called_once()
            mock_conn.close.assert_called_once()


class TestDatabaseIterable:
    """Test DatabaseIterable wrapper."""

    def test_read_single_row(self):
        """Test reading single row."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)
        row = iterable.read()

        assert row == {"id": 1, "name": "test"}
        mock_driver.iterate.assert_called_once()

    def test_read_bulk(self):
        """Test reading multiple rows."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": i} for i in range(5)])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)
        rows = iterable.read_bulk(3)

        assert len(rows) == 3
        assert rows[0] == {"id": 0}
        assert rows[1] == {"id": 1}
        assert rows[2] == {"id": 2}

    def test_reset_not_supported(self):
        """Test reset() raises NotImplementedError."""
        mock_driver = MagicMock(spec=DBDriver)
        iterable = DatabaseIterable(mock_driver)

        with pytest.raises(NotImplementedError, match="Reset is not supported"):
            iterable.reset()

    def test_close(self):
        """Test close() closes driver."""
        mock_driver = MagicMock(spec=DBDriver)
        iterable = DatabaseIterable(mock_driver)
        iterable._iterator = iter([{"id": 1}])

        iterable.close()

        mock_driver.close.assert_called_once()
        assert iterable._iterator is None

    def test_context_manager(self):
        """Test context manager usage."""
        mock_driver = MagicMock(spec=DBDriver)
        iterable = DatabaseIterable(mock_driver)

        with iterable:
            pass

        mock_driver.close.assert_called_once()

    def test_metrics_property(self):
        """Test metrics property delegates to driver."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.metrics = {"rows_read": 10, "elapsed_seconds": 1.5}
        iterable = DatabaseIterable(mock_driver)

        metrics = iterable.metrics
        assert metrics == {"rows_read": 10, "elapsed_seconds": 1.5}

    def test_is_streaming(self):
        """Test is_streaming() returns True."""
        mock_driver = MagicMock(spec=DBDriver)
        iterable = DatabaseIterable(mock_driver)
        assert iterable.is_streaming() is True

    def test_is_flat(self):
        """Test is_flat() returns True."""
        mock_driver = MagicMock(spec=DBDriver)
        iterable = DatabaseIterable(mock_driver)
        assert iterable.is_flat() is True


class TestDriverRegistry:
    """Test driver registry functionality."""

    def test_register_driver(self):
        """Test registering a driver."""

        # Create a mock driver class
        class MockDriver(DBDriver):
            def connect(self):
                pass

            def iterate(self) -> Iterator:
                yield {}

        register_driver("mock", MockDriver)
        assert get_driver("mock") == MockDriver

    def test_get_driver(self):
        """Test getting a registered driver."""
        driver_class = get_driver("postgres")
        # Should return PostgresDriver if psycopg2 is available, None otherwise
        assert driver_class is None or driver_class == PostgresDriver

    def test_list_drivers(self):
        """Test listing registered drivers."""
        drivers = list_drivers()
        assert isinstance(drivers, list)
        # May include postgres if psycopg2 is installed

    def test_is_database_engine(self):
        """Test checking if engine is a database engine."""

        # Register a test driver
        class TestDriver(DBDriver):
            def connect(self):
                pass

            def iterate(self) -> Iterator:
                yield {}

        register_driver("testdb", TestDriver)
        assert is_database_engine("testdb") is True
        assert is_database_engine("internal") is False
        assert is_database_engine("duckdb") is False


class TestOpenIterableIntegration:
    """Test integration with open_iterable()."""

    def test_open_iterable_with_postgres_engine(self):
        """Test open_iterable() with postgres engine."""
        with patch("iterable.helpers.detect.get_driver") as mock_get_driver:
            with patch("iterable.helpers.detect.PostgresDriver") as mock_postgres_driver_class:
                mock_driver = MagicMock()
                mock_postgres_driver_class.return_value = mock_driver
                mock_get_driver.return_value = mock_postgres_driver_class

                from iterable.helpers.detect import open_iterable

                iterable = open_iterable(
                    "postgresql://localhost/db",
                    engine="postgres",
                    iterableargs={"query": "users"},
                )

                assert isinstance(iterable, DatabaseIterable)
                mock_postgres_driver_class.assert_called_once()

    def test_open_iterable_database_engine_not_available(self):
        """Test open_iterable() when database engine is not available."""
        with patch("iterable.helpers.detect.get_driver") as mock_get_driver:
            mock_get_driver.return_value = None

            from iterable.helpers.detect import open_iterable

            with pytest.raises(ValueError, match="is not available"):
                open_iterable("postgresql://localhost/db", engine="postgres", iterableargs={"query": "users"})


class TestConvertIntegration:
    """Test integration with convert()."""

    def test_convert_from_database_to_file(self):
        """Test convert() from database source to file."""
        with patch("iterable.helpers.detect.get_driver") as mock_get_driver:
            with patch("iterable.helpers.detect.PostgresDriver") as mock_postgres_driver_class:
                mock_driver = MagicMock()
                mock_driver.is_connected = True
                mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
                mock_driver._start_metrics = MagicMock()
                mock_postgres_driver_class.return_value = mock_driver
                mock_get_driver.return_value = mock_postgres_driver_class

                import os
                import tempfile

                from iterable.convert import convert

                with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    convert(
                        fromfile="postgresql://localhost/db",
                        tofile=tmp_path,
                        iterableargs={"engine": "postgres", "query": "users"},
                    )

                    assert os.path.exists(tmp_path)
                    with open(tmp_path) as f:
                        content = f.read()
                        assert "test" in content
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)


class TestPipelineIntegration:
    """Test integration with pipeline()."""

    def test_pipeline_with_database_source(self):
        """Test pipeline() with database source."""
        with patch("iterable.helpers.detect.get_driver") as mock_get_driver:
            with patch("iterable.helpers.detect.PostgresDriver") as mock_postgres_driver_class:
                mock_driver = MagicMock()
                mock_driver.is_connected = True
                mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
                mock_driver._start_metrics = MagicMock()
                mock_postgres_driver_class.return_value = mock_driver
                mock_get_driver.return_value = mock_postgres_driver_class

                import os
                import tempfile

                from iterable.helpers.detect import open_iterable
                from iterable.pipeline import Pipeline

                with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    source = open_iterable(
                        "postgresql://localhost/db",
                        engine="postgres",
                        iterableargs={"query": "users"},
                    )
                    dest = open_iterable(tmp_path, mode="w")

                    pipeline = Pipeline(source, dest)
                    result = pipeline.run()

                    assert result.rows_processed > 0
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)


class TestDataFrameBridges:
    """Test DataFrame bridge methods with database sources."""

    def test_to_pandas(self):
        """Test .to_pandas() with database source."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)

        try:
            df = iterable.to_pandas()
            assert len(df) == 1
            assert "id" in df.columns
            assert "name" in df.columns
        except ImportError:
            pytest.skip("pandas not installed")

    def test_to_pandas_chunked(self):
        """Test .to_pandas() with chunksize."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": i} for i in range(5)])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)

        try:
            chunks = iterable.to_pandas(chunksize=2)
            chunk_list = list(chunks)
            assert len(chunk_list) == 3  # 2, 2, 1
            assert len(chunk_list[0]) == 2
        except ImportError:
            pytest.skip("pandas not installed")

    def test_to_polars(self):
        """Test .to_polars() with database source."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)

        try:
            df = iterable.to_polars()
            assert len(df) == 1
            assert "id" in df.columns
            assert "name" in df.columns
        except ImportError:
            pytest.skip("polars not installed")

    def test_to_dask(self):
        """Test .to_dask() with database source."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([{"id": 1, "name": "test"}])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)

        try:
            df = iterable.to_dask()
            assert len(df) == 1
            assert "id" in df.columns
            assert "name" in df.columns
        except ImportError:
            pytest.skip("dask not installed")


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_result_set(self):
        """Test handling of empty result sets."""
        mock_driver = MagicMock(spec=DBDriver)
        mock_driver.is_connected = True
        mock_driver.iterate.return_value = iter([])
        mock_driver._start_metrics = MagicMock()

        iterable = DatabaseIterable(mock_driver)

        with pytest.raises(StopIteration):
            iterable.read()

    def test_connection_failure(self):
        """Test handling of connection failures."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_psycopg2.connect.side_effect = Exception("Connection refused")

            driver = PostgresDriver("postgresql://localhost/db", query="users")
            with pytest.raises(ConnectionError, match="Failed to connect"):
                driver.connect()

    def test_invalid_query(self):
        """Test handling of invalid queries."""
        with patch("iterable.db.postgres.psycopg2") as mock_psycopg2:
            mock_conn = MagicMock()
            mock_psycopg2.connect.return_value = mock_conn
            mock_cursor = MagicMock()
            mock_cursor.execute.side_effect = Exception("syntax error")
            mock_conn.cursor.return_value = mock_cursor

            driver = PostgresDriver("postgresql://localhost/db", query="INVALID SQL", on_error="raise")
            driver.connect()

            with pytest.raises(Exception, match="syntax error"):
                list(driver.iterate())

    def test_malformed_connection_string(self):
        """Test handling of malformed connection strings."""
        driver = PostgresDriver(123, query="users")  # Not a string or connection object
        with pytest.raises(ValueError, match="must be a connection string"):
            driver.connect()
