# Factory Method Design for BaseFileIterable

## Design Goals

1. **Backward Compatibility**: Keep existing `__init__` method working
2. **Clear Intent**: Factory methods make source type explicit
3. **Type Safety**: Better type hints and validation
4. **Easier Testing**: Isolated initialization paths
5. **Better Documentation**: Clear examples for each pattern

## Factory Method API Design

### 1. File-Based Factory Method

```python
@classmethod
def from_file(
    cls,
    filename: str,
    mode: str = "r",
    encoding: str = "utf8",
    binary: bool = False,
    noopen: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from a file path.
    
    Args:
        filename: Path to the file
        mode: File mode ('r', 'w', 'rb', 'wb')
        encoding: Text encoding (default: 'utf8')
        binary: Whether to open in binary mode
        noopen: If True, don't open the file immediately
        **options: Additional options (on_error, error_log, etc.)
    
    Returns:
        BaseFileIterable instance configured for file-based access
    
    Example:
        >>> iterable = BaseFileIterable.from_file("data.csv", encoding="utf-8")
    """
```

**Benefits:**
- Clear that we're working with a file
- Can validate filename exists (optional)
- Type-safe: filename is required, not optional

### 2. Stream-Based Factory Method

```python
@classmethod
def from_stream(
    cls,
    stream: typing.IO[Any],
    encoding: str = "utf8",
    binary: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from an open stream.
    
    Args:
        stream: Open file-like object (already opened)
        encoding: Text encoding (default: 'utf8')
        binary: Whether stream is binary
        **options: Additional options (on_error, error_log, etc.)
    
    Returns:
        BaseFileIterable instance configured for stream-based access
    
    Example:
        >>> with open("data.csv") as f:
        ...     iterable = BaseFileIterable.from_stream(f)
    """
```

**Benefits:**
- Clear that stream must be pre-opened
- No filename parameter (not applicable)
- Type-safe: stream is required

### 3. Codec-Based Factory Method

```python
@classmethod
def from_codec(
    cls,
    codec: BaseCodec,
    encoding: str = "utf8",
    noopen: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from a codec.
    
    Args:
        codec: Codec instance (e.g., GZIPCodec, BZIP2Codec)
        encoding: Text encoding (default: 'utf8')
        noopen: If True, don't open the codec immediately
        **options: Additional options (on_error, error_log, etc.)
    
    Returns:
        BaseFileIterable instance configured for codec-based access
    
    Example:
        >>> from iterable.codecs.gzipcodec import GZIPCodec
        >>> codec = GZIPCodec(filename="data.csv.gz")
        >>> iterable = BaseFileIterable.from_codec(codec)
    """
```

**Benefits:**
- Clear that codec must be pre-configured
- Can validate codec type
- Type-safe: codec is required

## Internal Refactoring

### Helper Methods for Initialization

To support factory methods and improve `__init__`, we'll create internal helper methods:

```python
def _init_source(
    self,
    filename: str | None = None,
    stream: typing.IO[Any] | None = None,
    codec: BaseCodec | None = None,
    noopen: bool = False,
) -> None:
    """Initialize the data source (file, stream, or codec).
    
    Validates that exactly one source is provided and sets up the file object.
    """
    # Count provided sources
    sources = [filename, stream, codec]
    provided = [s for s in sources if s is not None]
    
    if len(provided) == 0:
        raise ValueError("BaseFileIterable requires filename, stream, or codec")
    if len(provided) > 1:
        raise ValueError(
            f"BaseFileIterable requires exactly one source. "
            f"Provided: {[type(s).__name__ for s in provided]}"
        )
    
    # Determine source type
    if stream is not None:
        self.stype = ITERABLE_TYPE_STREAM
        self.fobj = stream
    elif filename is not None:
        self.stype = ITERABLE_TYPE_FILE
        self.filename = filename
        if not noopen:
            self.open()
    elif codec is not None:
        self.stype = ITERABLE_TYPE_CODEC
        self.codec = codec
        if not noopen:
            self.codec.open()
            self.fobj = self.codec.fileobj()
            if self.datamode == "text":
                self.fobj = self.codec.textIO(encoding=self.encoding)
    else:
        # Should never reach here due to validation above
        raise ValueError("BaseFileIterable requires filename, stream, or codec")

def _init_error_handling(self, options: dict[str, Any]) -> None:
    """Initialize error handling configuration.
    
    Separates error handling setup from source initialization.
    """
    self._on_error = options.get("on_error", "raise")
    self._error_log = options.get("error_log", None)
    self._error_log_file = None
    self._error_log_owned = False
    
    # Validate error policy
    if self._on_error not in ("raise", "skip", "warn"):
        raise ValueError(
            f"Invalid 'on_error' value: '{self._on_error}'. "
            f"Valid values are: 'raise', 'skip', 'warn'"
        )
    
    # Setup error logging
    if self._error_log is not None:
        if isinstance(self._error_log, str):
            self._error_log_file = None
            self._error_log_owned = True
        elif isinstance(self._error_log, ErrorLogWriter):
            self._error_log_file = self._error_log
            self._error_log_owned = False
        else:
            raise ValueError(
                f"Invalid 'error_log' value: must be file path (str) or "
                f"file-like object with write() method, "
                f"got {type(self._error_log).__name__}"
            )

def _apply_options(self, options: dict[str, Any], protected: set[str] | None = None) -> None:
    """Apply options dictionary with validation.
    
    Args:
        options: Dictionary of options to apply
        protected: Set of attribute names that cannot be overridden
    """
    if protected is None:
        protected = {
            "stype", "fobj", "_on_error", "_error_log", "_error_log_file",
            "_error_log_owned", "_closed"
        }
    
    for key, value in options.items():
        if key in protected:
            raise ValueError(
                f"Cannot override protected attribute '{key}' via options. "
                f"Use the appropriate parameter or factory method instead."
            )
        setattr(self, key, value)
```

## Refactored __init__ Method

```python
def __init__(
    self,
    filename: str | None = None,
    stream: typing.IO[Any] | None = None,
    codec: BaseCodec | None = None,
    binary: bool = False,
    encoding: str = "utf8",
    noopen: bool = False,
    mode: str = "r",
    options: dict[str, Any] | None = None,
) -> None:
    """Initialize BaseFileIterable.
    
    This method is maintained for backward compatibility. For new code,
    consider using factory methods:
    - BaseFileIterable.from_file() for file-based access
    - BaseFileIterable.from_stream() for stream-based access
    - BaseFileIterable.from_codec() for codec-based access
    
    Args:
        filename: Path to file (mutually exclusive with stream/codec)
        stream: Open file-like object (mutually exclusive with filename/codec)
        codec: Codec instance (mutually exclusive with filename/stream)
        binary: Whether to use binary mode
        encoding: Text encoding (default: 'utf8')
        noopen: If True, don't open the source immediately
        mode: File mode ('r', 'w', 'rb', 'wb')
        options: Additional options dictionary
    
    Raises:
        ValueError: If multiple sources provided or no source provided
    """
    super().__init__()  # Initialize BaseIterable (_closed flag)
    
    if options is None:
        options = {}
    
    # Set basic attributes
    self.filename = filename
    self.noopen = noopen
    self.encoding = encoding
    self.binary = binary
    self.mode = mode
    self.codec = codec
    self.fobj = None
    
    # Initialize source (validates and sets up file object)
    self._init_source(filename, stream, codec, noopen)
    
    # Initialize error handling
    self._init_error_handling(options)
    
    # Apply additional options (with protection)
    self._apply_options(options)
```

## Factory Method Implementation

```python
@classmethod
def from_file(
    cls,
    filename: str,
    mode: str = "r",
    encoding: str = "utf8",
    binary: bool = False,
    noopen: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from a file path."""
    return cls(
        filename=filename,
        stream=None,
        codec=None,
        binary=binary,
        encoding=encoding,
        noopen=noopen,
        mode=mode,
        options=options,
    )

@classmethod
def from_stream(
    cls,
    stream: typing.IO[Any],
    encoding: str = "utf8",
    binary: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from an open stream."""
    return cls(
        filename=None,
        stream=stream,
        codec=None,
        binary=binary,
        encoding=encoding,
        noopen=False,  # Stream is already open
        mode="r",  # Not applicable for streams
        options=options,
    )

@classmethod
def from_codec(
    cls,
    codec: BaseCodec,
    encoding: str = "utf8",
    noopen: bool = False,
    **options: Any,
) -> "BaseFileIterable":
    """Create BaseFileIterable from a codec."""
    return cls(
        filename=None,
        stream=None,
        codec=codec,
        binary=False,  # Codec handles binary/text
        encoding=encoding,
        noopen=noopen,
        mode="r",  # Codec handles mode
        options=options,
    )
```

## Benefits of This Design

1. **Backward Compatible**: Existing `__init__` calls continue to work
2. **Clear API**: Factory methods make intent explicit
3. **Better Validation**: Can validate source type at factory method level
4. **Type Safety**: Required parameters are explicit in factory methods
5. **Better Organization**: Internal helper methods separate concerns
6. **Protected Attributes**: Options can't override critical settings
7. **Easier Testing**: Each initialization path can be tested independently
8. **Better Documentation**: Factory methods have clear docstrings and examples

## Migration Path

1. **Phase 1**: Add factory methods and internal helpers (backward compatible)
2. **Phase 2**: Update documentation to recommend factory methods
3. **Phase 3**: Update examples to use factory methods
4. **Phase 4**: (Optional) Deprecate direct `__init__` usage in future major version

## Example Usage

### Old Way (Still Works)
```python
iterable = CSVIterable(filename="data.csv", encoding="utf-8")
```

### New Way (Recommended)
```python
iterable = CSVIterable.from_file("data.csv", encoding="utf-8")
```

### With Error Handling
```python
iterable = CSVIterable.from_file(
    "data.csv",
    encoding="utf-8",
    on_error="skip",
    error_log="errors.log"
)
```

### With Codec
```python
from iterable.codecs.gzipcodec import GZIPCodec

codec = GZIPCodec(filename="data.csv.gz")
iterable = CSVIterable.from_codec(codec, encoding="utf-8")
```

## Testing Strategy

1. **Test Factory Methods**: Each factory method should be tested independently
2. **Test Helper Methods**: `_init_source`, `_init_error_handling`, `_apply_options`
3. **Test Validation**: Multiple sources, no sources, protected attributes
4. **Test Backward Compatibility**: Existing `__init__` calls still work
5. **Test Integration**: Factory methods work with all format implementations

## Next Steps

1. Implement factory methods in `BaseFileIterable`
2. Implement internal helper methods
3. Refactor `__init__` to use helpers
4. Add unit tests for factory methods
5. Update documentation with examples
6. Update format implementations to use factory methods (optional, for consistency)
