# Connection Pooling Design for Database Formats

## Executive Summary

This document designs a connection pooling system for IterableData database drivers (PostgreSQL, MySQL, MongoDB, Elasticsearch, etc.) to improve performance when processing multiple queries or files from the same database.

## Current State

### Database Driver Architecture

Each database driver (`PostgresDriver`, `MySQLDriver`, `MongoDriver`, etc.) inherits from `DBDriver` base class:

- **Connection Management**: Each driver instance creates its own connection
- **Connection Lifecycle**: Connection created in `connect()`, closed in `close()`
- **No Reuse**: Each new driver instance creates a new connection
- **No Pooling**: Connections are not reused across instances

### Current Connection Pattern

```python
# Each call creates a new connection
with open_iterable('postgresql://...', iterableargs={'query': 'SELECT ...'}) as source:
    for row in source:
        process(row)
# Connection closed

# Next call creates another new connection
with open_iterable('postgresql://...', iterableargs={'query': 'SELECT ...'}) as source:
    for row in source:
        process(row)
# Connection closed again
```

**Problem**: Creating new connections for each query is expensive, especially for:
- High-frequency queries
- Multiple queries to the same database
- Short-lived queries where connection overhead dominates

## Use Cases for Connection Pooling

### 1. Multiple Queries to Same Database

**Scenario**: Process multiple queries from the same database

```python
# Current (creates 3 separate connections)
queries = ['SELECT * FROM table1', 'SELECT * FROM table2', 'SELECT * FROM table3']
for query in queries:
    with open_iterable('postgresql://...', iterableargs={'query': query}) as source:
        process(source)

# With pooling (reuses connections from pool)
# Same code, but connections are reused automatically
```

**Benefit**: Reduced connection overhead, faster execution

### 2. Concurrent Database Access

**Scenario**: Process multiple queries concurrently

```python
# With pooling (pool handles concurrent connections)
import concurrent.futures

queries = ['SELECT * FROM table1', 'SELECT * FROM table2', 'SELECT * FROM table3']
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(process_query, 'postgresql://...', query)
        for query in queries
    ]
    # Pool provides connections for concurrent access
```

**Benefit**: Better resource utilization, improved throughput

### 3. Long-Running Processes

**Scenario**: ETL pipeline processing many files/queries

```python
# With pooling (connections reused across many operations)
for file in many_files:
    with open_iterable(f'postgresql://...', iterableargs={'query': f'SELECT * FROM {file}'}) as source:
        process(source)
# Connections reused from pool, not recreated each time
```

**Benefit**: Consistent performance, reduced database load

## Design Approach

### Option 1: Driver-Level Pooling (Recommended)

Each database driver manages its own connection pool:

```python
# iterable/db/pooling.py

from typing import Any
from threading import Lock
from queue import Queue, Empty
import time

class ConnectionPool:
    """Thread-safe connection pool for database drivers"""
    
    def __init__(
        self,
        connection_factory: callable,
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 30.0,
        max_idle: float = 300.0,  # 5 minutes
    ):
        self._factory = connection_factory
        self._min_size = min_size
        self._max_size = max_size
        self._timeout = timeout
        self._max_idle = max_idle
        
        self._pool: Queue[tuple[Any, float]] = Queue()  # (connection, created_time)
        self._created = 0  # Number of connections created
        self._lock = Lock()
        
        # Pre-populate pool with min_size connections
        for _ in range(min_size):
            conn = self._factory()
            self._pool.put((conn, time.time()))
            self._created += 1
    
    def acquire(self) -> Any:
        """Acquire a connection from the pool"""
        try:
            # Try to get existing connection
            conn, created_time = self._pool.get_nowait()
            
            # Check if connection is stale
            if time.time() - created_time > self._max_idle:
                # Connection too old, create new one
                try:
                    conn.close()
                except Exception:
                    pass
                conn = self._factory()
                created_time = time.time()
            
            return conn, created_time
        except Empty:
            # No connection available, create new one if under max_size
            with self._lock:
                if self._created < self._max_size:
                    conn = self._factory()
                    self._created += 1
                    return conn, time.time()
                else:
                    # Wait for connection to become available
                    conn, created_time = self._pool.get(timeout=self._timeout)
                    return conn, created_time
    
    def release(self, conn: Any, created_time: float) -> None:
        """Release a connection back to the pool"""
        # Check if connection is still valid
        if self._is_valid(conn):
            self._pool.put((conn, created_time))
        else:
            # Connection invalid, create new one
            with self._lock:
                self._created -= 1
            try:
                conn.close()
            except Exception:
                pass
    
    def _is_valid(self, conn: Any) -> bool:
        """Check if connection is still valid"""
        # Database-specific validation
        try:
            # Try a simple operation (ping, SELECT 1, etc.)
            return True  # Simplified - actual implementation varies by database
        except Exception:
            return False
    
    def close_all(self) -> None:
        """Close all connections in the pool"""
        while not self._pool.empty():
            try:
                conn, _ = self._pool.get_nowait()
                conn.close()
            except Exception:
                pass
        self._created = 0
```

### Option 2: Global Pool Registry

Centralized pool registry shared across all drivers:

```python
# iterable/db/pooling.py

_pools: dict[str, ConnectionPool] = {}
_pools_lock = Lock()

def get_pool(connection_string: str, driver_class: type[DBDriver]) -> ConnectionPool:
    """Get or create connection pool for a connection string"""
    pool_key = f"{driver_class.__name__}:{connection_string}"
    
    with _pools_lock:
        if pool_key not in _pools:
            def factory():
                driver = driver_class(connection_string)
                driver.connect()
                return driver.conn
            
            _pools[pool_key] = ConnectionPool(
                factory,
                min_size=1,
                max_size=10,
            )
        return _pools[pool_key]
```

### Option 3: Driver-Specific Pooling

Each driver implements its own pooling using database-specific libraries:

```python
# PostgreSQL uses psycopg2.pool
from psycopg2 import pool

class PostgresDriver(DBDriver):
    _pools: dict[str, pool.ThreadedConnectionPool] = {}
    
    def connect(self) -> None:
        if self.source not in self._pools:
            # Create pool
            self._pools[self.source] = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.source
            )
        
        self._pool = self._pools[self.source]
        self.conn = self._pool.getconn()
```

**Pros**: Uses database-specific optimizations  
**Cons**: Inconsistent API, more complex

## Recommended Approach: Hybrid

Combine Option 1 (Driver-Level Pooling) with Option 2 (Global Registry):

1. **Generic ConnectionPool class** - Works for all databases
2. **Global pool registry** - Manages pools per connection string
3. **Driver integration** - Drivers use pools transparently
4. **Database-specific optimizations** - Optional enhancements for specific databases

## Implementation Design

### 1. Connection Pool Interface

```python
# iterable/db/pooling.py

from abc import ABC, abstractmethod
from typing import Any, Callable
from threading import Lock
from queue import Queue, Empty
import time
import logging

logger = logging.getLogger(__name__)

class ConnectionPool(ABC):
    """Base class for connection pools"""
    
    @abstractmethod
    def acquire(self) -> Any:
        """Acquire a connection from the pool"""
        pass
    
    @abstractmethod
    def release(self, conn: Any) -> None:
        """Release a connection back to the pool"""
        pass
    
    @abstractmethod
    def close_all(self) -> None:
        """Close all connections in the pool"""
        pass

class SimpleConnectionPool(ConnectionPool):
    """Simple thread-safe connection pool"""
    
    def __init__(
        self,
        factory: Callable[[], Any],
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 30.0,
        max_idle: float = 300.0,
        validate: Callable[[Any], bool] | None = None,
    ):
        self._factory = factory
        self._min_size = min_size
        self._max_size = max_size
        self._timeout = timeout
        self._max_idle = max_idle
        self._validate = validate or (lambda conn: True)
        
        self._pool: Queue[tuple[Any, float]] = Queue()
        self._created = 0
        self._lock = Lock()
        
        # Pre-populate
        for _ in range(min_size):
            self._create_and_add()
    
    def _create_and_add(self) -> None:
        """Create a new connection and add to pool"""
        try:
            conn = self._factory()
            self._pool.put((conn, time.time()))
            with self._lock:
                self._created += 1
        except Exception as e:
            logger.warning(f"Failed to create connection: {e}")
    
    def acquire(self) -> Any:
        """Acquire a connection from the pool"""
        deadline = time.time() + self._timeout
        
        while time.time() < deadline:
            try:
                conn, created_time = self._pool.get_nowait()
                
                # Check if connection is stale
                if time.time() - created_time > self._max_idle:
                    try:
                        self._close_connection(conn)
                    except Exception:
                        pass
                    conn = self._factory()
                    created_time = time.time()
                
                # Validate connection
                if not self._validate(conn):
                    try:
                        self._close_connection(conn)
                    except Exception:
                        pass
                    conn = self._factory()
                    created_time = time.time()
                
                return conn, created_time
            except Empty:
                # No connection available, create new one if under max_size
                with self._lock:
                    if self._created < self._max_size:
                        conn = self._factory()
                        created_time = time.time()
                        self._created += 1
                        return conn, created_time
                
                # Wait a bit and retry
                time.sleep(0.1)
        
        raise TimeoutError(f"Failed to acquire connection within {self._timeout}s")
    
    def release(self, conn: Any, created_time: float) -> None:
        """Release a connection back to the pool"""
        if self._validate(conn):
            self._pool.put((conn, created_time))
        else:
            # Connection invalid, don't return to pool
            with self._lock:
                self._created -= 1
            try:
                self._close_connection(conn)
            except Exception:
                pass
    
    def _close_connection(self, conn: Any) -> None:
        """Close a connection (database-specific)"""
        if hasattr(conn, "close"):
            conn.close()
    
    def close_all(self) -> None:
        """Close all connections in the pool"""
        while not self._pool.empty():
            try:
                conn, _ = self._pool.get_nowait()
                self._close_connection(conn)
            except Exception:
                pass
        with self._lock:
            self._created = 0
```

### 2. Pool Registry

```python
# iterable/db/pooling.py (continued)

_pools: dict[str, ConnectionPool] = {}
_pools_lock = Lock()

def get_pool(
    pool_key: str,
    factory: Callable[[], Any],
    pool_config: dict[str, Any] | None = None
) -> ConnectionPool:
    """Get or create a connection pool"""
    if pool_config is None:
        pool_config = {}
    
    with _pools_lock:
        if pool_key not in _pools:
            _pools[pool_key] = SimpleConnectionPool(
                factory,
                min_size=pool_config.get("min_size", 1),
                max_size=pool_config.get("max_size", 10),
                timeout=pool_config.get("timeout", 30.0),
                max_idle=pool_config.get("max_idle", 300.0),
                validate=pool_config.get("validate"),
            )
        return _pools[pool_key]

def close_pool(pool_key: str) -> None:
    """Close a specific pool"""
    with _pools_lock:
        if pool_key in _pools:
            _pools[pool_key].close_all()
            del _pools[pool_key]

def close_all_pools() -> None:
    """Close all connection pools"""
    with _pools_lock:
        for pool in _pools.values():
            pool.close_all()
        _pools.clear()
```

### 3. Driver Integration

```python
# iterable/db/postgres.py (modified)

from .pooling import get_pool

class PostgresDriver(DBDriver):
    def __init__(self, source: str | Any, **kwargs: Any) -> None:
        super().__init__(source, **kwargs)
        self._use_pool = kwargs.get("use_pool", True)  # Enable pooling by default
        self._pool = None
        self._pooled_conn = None
        self._pooled_created_time = None
    
    def connect(self) -> None:
        """Establish database connection (with pooling support)"""
        if self._use_pool and isinstance(self.source, str):
            # Use connection pool
            pool_key = f"postgres:{self.source}"
            
            def factory():
                # Create new connection
                import psycopg2
                conn = psycopg2.connect(self.source, **self.kwargs.get("connect_args", {}))
                return conn
            
            self._pool = get_pool(pool_key, factory)
            self._pooled_conn, self._pooled_created_time = self._pool.acquire()
            self.conn = self._pooled_conn
        else:
            # Direct connection (no pooling)
            import psycopg2
            self.conn = psycopg2.connect(self.source, **self.kwargs.get("connect_args", {}))
        
        self._connected = True
    
    def close(self) -> None:
        """Close connection (return to pool if pooled)"""
        if self._pool and self._pooled_conn:
            # Return to pool
            self._pool.release(self._pooled_conn, self._pooled_created_time)
            self._pooled_conn = None
            self._pooled_created_time = None
        elif self.conn:
            # Direct close
            self.conn.close()
            self.conn = None
        
        self._connected = False
        self._closed = True
```

## Configuration

### Pool Configuration Options

```python
# Pool configuration via iterableargs
with open_iterable(
    'postgresql://...',
    iterableargs={
        'query': 'SELECT ...',
        'pool': {
            'enabled': True,  # Enable pooling (default: True)
            'min_size': 1,    # Minimum pool size (default: 1)
            'max_size': 10,   # Maximum pool size (default: 10)
            'timeout': 30.0,  # Timeout for acquiring connection (default: 30s)
            'max_idle': 300.0,  # Max idle time before connection closed (default: 5min)
        }
    }
) as source:
    for row in source:
        process(row)
```

### Global Pool Configuration

```python
# iterable/db/pooling.py

DEFAULT_POOL_CONFIG = {
    "min_size": 1,
    "max_size": 10,
    "timeout": 30.0,
    "max_idle": 300.0,
}

def configure_pooling(config: dict[str, Any]) -> None:
    """Configure default pool settings"""
    DEFAULT_POOL_CONFIG.update(config)
```

## Database-Specific Considerations

### PostgreSQL

- **Library**: `psycopg2` has built-in `pool.ThreadedConnectionPool`
- **Recommendation**: Use `psycopg2.pool` for PostgreSQL-specific optimizations
- **Validation**: Use `conn.closed` property or `SELECT 1` query

### MySQL

- **Library**: `pymysql` or `mysql-connector-python`
- **Recommendation**: Generic pool works well
- **Validation**: Use `conn.ping()` method

### MongoDB

- **Library**: `pymongo` has built-in connection pooling
- **Recommendation**: Use `pymongo.MongoClient` pooling (already built-in)
- **Note**: MongoDB client already pools connections internally

### Elasticsearch

- **Library**: `elasticsearch` client
- **Recommendation**: Generic pool works well
- **Validation**: Use `conn.ping()` method

### SQLite

- **Recommendation**: **No pooling needed** - SQLite is file-based, not network-based
- **Note**: Each instance can use the same file connection

## Performance Considerations

### Benefits

1. **Reduced Connection Overhead**: Reuse connections instead of creating new ones
2. **Better Resource Utilization**: Pool manages connection lifecycle
3. **Concurrent Access**: Pool handles multiple concurrent requests
4. **Connection Validation**: Automatic validation and cleanup of stale connections

### Overhead

1. **Pool Management**: Small overhead for pool operations (queue, locks)
2. **Connection Validation**: Validation adds small overhead
3. **Memory**: Pool keeps connections in memory

### When Pooling Helps

✅ **Good Use Cases**:
- Multiple queries to the same database
- High-frequency queries
- Concurrent database access
- Long-running processes with many database operations

❌ **Limited Benefit**:
- Single query operations
- Different databases (no reuse)
- Very long-lived connections (pooling overhead not worth it)

## Implementation Strategy

### Phase 1: Core Infrastructure

1. **Create `ConnectionPool` base class**
2. **Implement `SimpleConnectionPool`**
3. **Create pool registry**
4. **Add pool configuration options**

### Phase 2: Driver Integration

1. **Integrate with PostgreSQL driver**
2. **Integrate with MySQL driver**
3. **Integrate with MongoDB driver** (may use built-in pooling)
4. **Integrate with Elasticsearch driver**

### Phase 3: Optimization

1. **Database-specific pool implementations** (e.g., use `psycopg2.pool`)
2. **Connection validation improvements**
3. **Performance tuning** (pool sizes, timeouts)

## Testing Strategy

1. **Test pool creation and cleanup**
2. **Test connection acquisition and release**
3. **Test pool size limits** (min_size, max_size)
4. **Test connection validation** (stale connections)
5. **Test concurrent access** (thread safety)
6. **Test timeout behavior**
7. **Test pool configuration** (enabled/disabled)
8. **Performance benchmarks** (with vs without pooling)

## Examples

### Example 1: Basic Usage (Automatic Pooling)

```python
# Pooling enabled by default
with open_iterable(
    'postgresql://user:pass@host/db',
    iterableargs={'query': 'SELECT * FROM table1'}
) as source:
    for row in source:
        process(row)
# Connection returned to pool

# Next query reuses connection from pool
with open_iterable(
    'postgresql://user:pass@host/db',
    iterableargs={'query': 'SELECT * FROM table2'}
) as source:
    for row in source:
        process(row)
# Connection returned to pool again
```

### Example 2: Custom Pool Configuration

```python
with open_iterable(
    'postgresql://user:pass@host/db',
    iterableargs={
        'query': 'SELECT * FROM table',
        'pool': {
            'enabled': True,
            'min_size': 2,
            'max_size': 20,
            'timeout': 60.0,
            'max_idle': 600.0,
        }
    }
) as source:
    for row in source:
        process(row)
```

### Example 3: Disable Pooling

```python
# Disable pooling for this connection
with open_iterable(
    'postgresql://user:pass@host/db',
    iterableargs={
        'query': 'SELECT * FROM table',
        'pool': {'enabled': False}
    }
) as source:
    for row in source:
        process(row)
```

### Example 4: Concurrent Access

```python
import concurrent.futures

def process_query(query):
    with open_iterable(
        'postgresql://user:pass@host/db',
        iterableargs={'query': query}
    ) as source:
        return list(source)

queries = ['SELECT * FROM table1', 'SELECT * FROM table2', 'SELECT * FROM table3']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(process_query, queries)
    # Pool provides connections for concurrent access
```

## Migration Path

### Backward Compatibility

- **Pooling disabled by default initially** (opt-in)
- **Existing code continues to work** (no pooling)
- **Gradually enable by default** after testing

### Gradual Rollout

1. **Phase 1**: Implement pooling infrastructure (opt-in)
2. **Phase 2**: Enable pooling by default for new connections
3. **Phase 3**: Optimize pool configurations based on usage

## Conclusion

Connection pooling for database formats provides significant performance benefits for:

- **Multiple queries** to the same database
- **Concurrent access** patterns
- **High-frequency operations**

The recommended approach uses a **generic connection pool** with **database-specific optimizations** where beneficial. Pooling is **enabled by default** but can be **configured or disabled** per connection.

**Key Design Decisions**:
- Generic `ConnectionPool` class works for all databases
- Global pool registry manages pools per connection string
- Drivers integrate pooling transparently
- Configuration via `iterableargs['pool']` dictionary
- Backward compatible (can disable pooling)

**Next Steps**: Implement core pooling infrastructure, integrate with PostgreSQL driver first, then expand to other drivers.
