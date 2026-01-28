# Plugin System Architecture Design

## Executive Summary

This document designs a comprehensive plugin system architecture for IterableData that enables third-party developers to extend the library with custom formats, codecs, database drivers, validation rules, and other capabilities without modifying the core library code.

## Current State

### Existing Extensibility Mechanisms

1. **Format Registry** (`iterable/helpers/detect.py`)
   - `DATATYPE_REGISTRY`: Dictionary mapping format IDs to (module_path, class_name)
   - Lazy loading via `_load_symbol()` function
   - Manual registration required in core code

2. **Codec Registry** (`iterable/helpers/detect.py`)
   - `CODEC_REGISTRY`: Dictionary mapping codec IDs to (module_path, class_name)
   - Lazy loading via `_load_symbol()` function
   - Manual registration required in core code

3. **Database Driver Registry** (`iterable/db/__init__.py`)
   - `register_driver()` function for registering database drivers
   - `_DRIVER_REGISTRY`: Dictionary mapping engine names to driver classes
   - Manual registration in `_register_builtin_drivers()`

**Limitation**: All registrations require modifying core library files. No way for third-party plugins to register without forking the repository.

## Use Cases for Plugin System

### 1. Custom Format Support

**Scenario**: Third-party developer wants to add support for a proprietary format

```python
# Plugin package: iterabledata-plugin-customformat
from iterable.plugins import register_format

class CustomFormatIterable(BaseIterable):
    ...

# Auto-registration via entry points
# setup.py or pyproject.toml:
# [project.entry-points."iterabledata.formats"]
# customformat = "iterabledata_plugin_customformat:CustomFormatIterable"
```

### 2. Custom Codec Support

**Scenario**: Add support for a new compression algorithm

```python
# Plugin package: iterabledata-plugin-newcodec
from iterable.plugins import register_codec

class NewCodec(BaseCodec):
    ...

# Auto-registration via entry points
```

### 3. Custom Database Driver

**Scenario**: Add support for a new database system

```python
# Plugin package: iterabledata-plugin-newdb
from iterable.plugins import register_database_driver

class NewDBDriver(DBDriver):
    ...

# Auto-registration via entry points
```

### 4. Custom Validation Rules

**Scenario**: Domain-specific validation rules

```python
# Plugin package: iterabledata-plugin-validation
from iterable.plugins import register_validation_rule

def validate_custom_field(value):
    # Custom validation logic
    return is_valid, error_message

register_validation_rule("custom.rule", validate_custom_field)
```

### 5. Custom Engines

**Scenario**: Add a new processing engine (e.g., Spark, Polars)

```python
# Plugin package: iterabledata-plugin-spark
from iterable.plugins import register_engine

class SparkEngine:
    ...

register_engine("spark", SparkEngine)
```

## Design Principles

1. **Entry Point Based**: Use Python's entry point system (setuptools/pip) for discovery
2. **Lazy Loading**: Plugins loaded only when needed
3. **Backward Compatible**: Existing built-in formats/codecs continue to work
4. **Priority System**: Built-in plugins take precedence over third-party plugins
5. **Error Isolation**: Plugin errors don't crash core library
6. **Metadata Support**: Plugins can provide metadata (version, dependencies, etc.)

## Architecture Overview

### Core Components

1. **Plugin Registry** - Central registry for all plugin types
2. **Plugin Loader** - Discovers and loads plugins via entry points
3. **Plugin Manager** - Manages plugin lifecycle and metadata
4. **Plugin Base Classes** - Abstract base classes for plugin types

### Plugin Types

1. **Format Plugins** - Custom data formats
2. **Codec Plugins** - Custom compression codecs
3. **Database Driver Plugins** - Custom database drivers
4. **Validation Rule Plugins** - Custom validation rules
5. **Engine Plugins** - Custom processing engines
6. **Hook Plugins** - Custom hooks (validation, progress, etc.)

## Detailed Design

### 1. Plugin Registry System

```python
# iterable/plugins/registry.py

from typing import Any, Callable
from collections import defaultdict

class PluginRegistry:
    """Central registry for all plugin types"""
    
    def __init__(self):
        self._formats: dict[str, tuple[str, str]] = {}  # format_id -> (module, class)
        self._codecs: dict[str, tuple[str, str]] = {}  # codec_id -> (module, class)
        self._database_drivers: dict[str, tuple[str, str]] = {}  # engine -> (module, class)
        self._validation_rules: dict[str, Callable] = {}  # rule_name -> validator
        self._engines: dict[str, tuple[str, str]] = {}  # engine_name -> (module, class)
        self._metadata: dict[str, dict[str, Any]] = {}  # plugin_id -> metadata
        
    def register_format(
        self,
        format_id: str,
        module_path: str,
        class_name: str,
        metadata: dict[str, Any] | None = None
    ) -> None:
        """Register a format plugin"""
        if format_id in self._formats:
            raise ValueError(f"Format '{format_id}' already registered")
        self._formats[format_id] = (module_path, class_name)
        if metadata:
            self._metadata[f"format:{format_id}"] = metadata
    
    def register_codec(
        self,
        codec_id: str,
        module_path: str,
        class_name: str,
        metadata: dict[str, Any] | None = None
    ) -> None:
        """Register a codec plugin"""
        ...
    
    # Similar methods for other plugin types
```

### 2. Entry Point Discovery

```python
# iterable/plugins/loader.py

import importlib.metadata
from typing import Any

def discover_plugins() -> None:
    """Discover and register plugins via entry points"""
    registry = get_plugin_registry()
    
    # Discover format plugins
    try:
        for entry_point in importlib.metadata.entry_points(group="iterabledata.formats"):
            format_id = entry_point.name
            module_path, class_name = entry_point.value.split(":")
            registry.register_format(format_id, module_path, class_name)
    except Exception as e:
        logger.warning(f"Error discovering format plugins: {e}")
    
    # Discover codec plugins
    try:
        for entry_point in importlib.metadata.entry_points(group="iterabledata.codecs"):
            codec_id = entry_point.name
            module_path, class_name = entry_point.value.split(":")
            registry.register_codec(codec_id, module_path, class_name)
    except Exception as e:
        logger.warning(f"Error discovering codec plugins: {e}")
    
    # Similar for other plugin types
```

### 3. Plugin Base Classes

```python
# iterable/plugins/base.py

from abc import ABC, abstractmethod
from typing import Any

class FormatPlugin(ABC):
    """Base class for format plugins"""
    
    @abstractmethod
    @staticmethod
    def id() -> str:
        """Return format identifier"""
        pass
    
    @abstractmethod
    @staticmethod
    def fileexts() -> list[str]:
        """Return list of file extensions"""
        pass
    
    def get_metadata(self) -> dict[str, Any]:
        """Return plugin metadata"""
        return {
            "version": "1.0.0",
            "author": None,
            "description": None,
        }

class CodecPlugin(ABC):
    """Base class for codec plugins"""
    
    @abstractmethod
    @staticmethod
    def fileexts() -> list[str]:
        """Return list of file extensions"""
        pass

class DatabaseDriverPlugin(ABC):
    """Base class for database driver plugins"""
    
    @abstractmethod
    @staticmethod
    def engine_name() -> str:
        """Return engine identifier"""
        pass
```

### 4. Integration with Existing Systems

#### Format Detection Integration

```python
# iterable/helpers/detect.py

from ..plugins import get_plugin_registry, discover_plugins

# Discover plugins on first import
_discovered = False

def _ensure_plugins_discovered():
    global _discovered
    if not _discovered:
        discover_plugins()
        _discovered = True

def detect_file_type(filename: str | None = None, ...) -> FileTypeResult:
    _ensure_plugins_discovered()
    
    registry = get_plugin_registry()
    
    # Check built-in formats first (priority)
    result = _detect_builtin_formats(filename, ...)
    if result:
        return result
    
    # Check plugin formats
    for format_id, (module_path, class_name) in registry._formats.items():
        try:
            format_class = _load_symbol(module_path, class_name)
            if _matches_format(filename, format_class):
                return FileTypeResult(format_id=format_id, ...)
        except Exception as e:
            logger.warning(f"Error loading format plugin '{format_id}': {e}")
    
    # ... rest of detection logic
```

#### Registry Merging

```python
def get_format_registry() -> dict[str, tuple[str, str]]:
    """Get merged format registry (built-in + plugins)"""
    _ensure_plugins_discovered()
    
    # Start with built-in formats (take precedence)
    merged = DATATYPE_REGISTRY.copy()
    
    # Add plugin formats (don't override built-in)
    registry = get_plugin_registry()
    for format_id, value in registry._formats.items():
        if format_id not in merged:
            merged[format_id] = value
    
    return merged
```

## Entry Point Specification

### Format Plugins

```python
# Plugin package setup.py or pyproject.toml

# setup.py
setup(
    name="iterabledata-plugin-customformat",
    entry_points={
        "iterabledata.formats": [
            "customformat = iterabledata_plugin_customformat:CustomFormatIterable",
        ],
    },
)

# pyproject.toml
[project.entry-points."iterabledata.formats"]
customformat = "iterabledata_plugin_customformat:CustomFormatIterable"
```

### Codec Plugins

```python
[project.entry-points."iterabledata.codecs"]
newcodec = "iterabledata_plugin_newcodec:NewCodec"
```

### Database Driver Plugins

```python
[project.entry-points."iterabledata.database_drivers"]
newdb = "iterabledata_plugin_newdb:NewDBDriver"
```

### Validation Rule Plugins

```python
[project.entry-points."iterabledata.validation_rules"]
custom.rule = "iterabledata_plugin_validation:validate_custom_field"
```

## Plugin API

### Registration API

```python
# iterable/plugins/__init__.py

from .registry import PluginRegistry

_registry = PluginRegistry()

def get_plugin_registry() -> PluginRegistry:
    """Get the global plugin registry"""
    return _registry

def register_format(
    format_id: str,
    format_class: type[BaseIterable],
    fileexts: list[str] | None = None,
    metadata: dict[str, Any] | None = None
) -> None:
    """Register a format plugin programmatically"""
    module_path = format_class.__module__
    class_name = format_class.__name__
    _registry.register_format(format_id, module_path, class_name, metadata)
    
    # Also register file extensions if provided
    if fileexts:
        for ext in fileexts:
            _registry.register_format(ext, module_path, class_name)

def register_codec(
    codec_id: str,
    codec_class: type[BaseCodec],
    fileexts: list[str] | None = None,
    metadata: dict[str, Any] | None = None
) -> None:
    """Register a codec plugin programmatically"""
    ...

# Similar for other plugin types
```

### Usage Examples

#### Example 1: Format Plugin

```python
# Plugin package: iterabledata-plugin-customformat
from iterable.base import BaseIterable
from iterable.plugins import register_format

class CustomFormatIterable(BaseIterable):
    @staticmethod
    def id() -> str:
        return "customformat"
    
    @staticmethod
    def fileexts() -> list[str]:
        return [".custom", ".cf"]
    
    def read(self, skip_empty: bool = True) -> dict:
        # Implementation
        ...

# Auto-registration via entry point (preferred)
# Or manual registration:
register_format("customformat", CustomFormatIterable, [".custom", ".cf"])
```

#### Example 2: Codec Plugin

```python
# Plugin package: iterabledata-plugin-newcodec
from iterable.codecs.base import BaseCodec
from iterable.plugins import register_codec

class NewCodec(BaseCodec):
    @staticmethod
    def fileexts() -> list[str]:
        return [".nc", ".newcodec"]
    
    def open(self) -> None:
        # Implementation
        ...

register_codec("newcodec", NewCodec, [".nc", ".newcodec"])
```

#### Example 3: Database Driver Plugin

```python
# Plugin package: iterabledata-plugin-newdb
from iterable.db.base import DBDriver
from iterable.plugins import register_database_driver

class NewDBDriver(DBDriver):
    @staticmethod
    def engine_name() -> str:
        return "newdb"
    
    def connect(self, connection_string: str, **kwargs) -> None:
        # Implementation
        ...

register_database_driver("newdb", NewDBDriver)
```

## Plugin Discovery and Loading

### Lazy Discovery

Plugins are discovered lazily on first use:

```python
# iterable/plugins/loader.py

_discovered = False

def discover_plugins(force: bool = False) -> None:
    """Discover plugins via entry points"""
    global _discovered
    if _discovered and not force:
        return
    
    registry = get_plugin_registry()
    
    # Discover all plugin types
    _discover_format_plugins(registry)
    _discover_codec_plugins(registry)
    _discover_database_driver_plugins(registry)
    _discover_validation_rule_plugins(registry)
    _discover_engine_plugins(registry)
    
    _discovered = True

def _discover_format_plugins(registry: PluginRegistry) -> None:
    """Discover format plugins"""
    try:
        for entry_point in importlib.metadata.entry_points(group="iterabledata.formats"):
            try:
                # Load the class to validate it
                module_path, class_name = entry_point.value.split(":")
                format_class = _load_symbol(module_path, class_name)
                
                # Get format ID from class or entry point name
                format_id = entry_point.name
                if hasattr(format_class, "id"):
                    format_id = format_class.id()
                
                # Register
                registry.register_format(format_id, module_path, class_name)
                
                # Register file extensions
                if hasattr(format_class, "fileexts"):
                    for ext in format_class.fileexts():
                        if ext.startswith("."):
                            ext = ext[1:]  # Remove leading dot
                        registry.register_format(ext, module_path, class_name)
                        
            except Exception as e:
                logger.warning(f"Failed to load format plugin '{entry_point.name}': {e}")
    except Exception as e:
        logger.warning(f"Error discovering format plugins: {e}")
```

### Error Handling

```python
def _load_plugin_safely(module_path: str, class_name: str) -> Any | None:
    """Safely load a plugin class, returning None on error"""
    try:
        return _load_symbol(module_path, class_name)
    except ImportError as e:
        logger.warning(f"Plugin '{module_path}.{class_name}' not available: {e}")
        return None
    except Exception as e:
        logger.warning(f"Error loading plugin '{module_path}.{class_name}': {e}")
        return None
```

## Plugin Metadata

### Metadata Structure

```python
PluginMetadata = TypedDict("PluginMetadata", {
    "version": str,
    "author": str | None,
    "description": str | None,
    "dependencies": list[str] | None,
    "license": str | None,
    "homepage": str | None,
})

# Example
metadata = {
    "version": "1.0.0",
    "author": "Plugin Author",
    "description": "Custom format plugin",
    "dependencies": ["some-package>=1.0"],
    "license": "MIT",
    "homepage": "https://github.com/author/plugin",
}
```

### Metadata Access

```python
def get_plugin_metadata(plugin_type: str, plugin_id: str) -> dict[str, Any] | None:
    """Get metadata for a plugin"""
    registry = get_plugin_registry()
    return registry._metadata.get(f"{plugin_type}:{plugin_id}")

def list_plugins(plugin_type: str | None = None) -> dict[str, list[str]]:
    """List all registered plugins"""
    registry = get_plugin_registry()
    result = {}
    
    if plugin_type is None or plugin_type == "formats":
        result["formats"] = list(registry._formats.keys())
    if plugin_type is None or plugin_type == "codecs":
        result["codecs"] = list(registry._codecs.keys())
    # ... etc
    
    return result
```

## Plugin Lifecycle

### Initialization

1. **Import Time**: Core library imports, registries initialized
2. **First Use**: Plugins discovered via entry points (lazy)
3. **Registration**: Plugins registered in registry
4. **Validation**: Plugin classes validated (check for required methods)

### Runtime

1. **Lazy Loading**: Plugin classes loaded only when needed
2. **Error Isolation**: Plugin errors don't crash core library
3. **Fallback**: Built-in formats take precedence over plugins

### Cleanup

1. **No explicit cleanup needed**: Plugins are stateless
2. **Resource cleanup**: Handled by plugin classes themselves

## Priority and Conflict Resolution

### Priority Order

1. **Built-in formats/codecs** - Highest priority
2. **Manually registered plugins** - Medium priority
3. **Entry point plugins** - Lowest priority

### Conflict Resolution

```python
def register_format(format_id: str, ...) -> None:
    """Register format with conflict resolution"""
    registry = get_plugin_registry()
    
    # Check if already registered
    if format_id in registry._formats:
        existing = registry._formats[format_id]
        # Check if it's built-in
        if format_id in DATATYPE_REGISTRY:
            logger.warning(
                f"Format '{format_id}' is built-in. "
                f"Plugin registration ignored."
            )
            return
        
        # Warn about override
        logger.warning(
            f"Format '{format_id}' already registered. "
            f"Overriding previous registration."
        )
    
    registry.register_format(format_id, ...)
```

## Testing Strategy

### Plugin Testing

```python
# tests/test_plugins.py

def test_format_plugin_registration():
    """Test format plugin registration"""
    from iterable.plugins import register_format, get_plugin_registry
    
    class TestFormat(BaseIterable):
        @staticmethod
        def id() -> str:
            return "testformat"
    
    register_format("testformat", TestFormat)
    registry = get_plugin_registry()
    assert "testformat" in registry._formats

def test_plugin_discovery():
    """Test plugin discovery via entry points"""
    # Mock entry points
    # Verify plugins are discovered and registered

def test_plugin_priority():
    """Test that built-in formats take precedence"""
    # Register plugin with same ID as built-in
    # Verify built-in is used

def test_plugin_error_isolation():
    """Test that plugin errors don't crash core"""
    # Register plugin that raises errors
    # Verify core library continues to work
```

## Migration Path

### Phase 1: Core Infrastructure

1. Create `iterable/plugins/` module
2. Implement `PluginRegistry` class
3. Implement plugin discovery via entry points
4. Add plugin registration APIs

### Phase 2: Integration

1. Integrate with format detection
2. Integrate with codec detection
3. Integrate with database driver registry
4. Update existing registries to use plugin system

### Phase 3: Documentation and Examples

1. Create plugin development guide
2. Add plugin examples
3. Document entry point specification
4. Create plugin template/tooling

## Examples

### Example 1: Complete Format Plugin Package

```python
# iterabledata-plugin-customformat/setup.py
from setuptools import setup

setup(
    name="iterabledata-plugin-customformat",
    version="1.0.0",
    py_modules=["iterabledata_plugin_customformat"],
    install_requires=["iterabledata>=1.0"],
    entry_points={
        "iterabledata.formats": [
            "customformat = iterabledata_plugin_customformat:CustomFormatIterable",
        ],
    },
)

# iterabledata-plugin-customformat/iterabledata_plugin_customformat.py
from iterable.base import BaseIterable
from iterable.types import Row

class CustomFormatIterable(BaseIterable):
    @staticmethod
    def id() -> str:
        return "customformat"
    
    @staticmethod
    def fileexts() -> list[str]:
        return [".custom", ".cf"]
    
    def read(self, skip_empty: bool = True) -> Row:
        # Implementation
        ...
    
    def write(self, record: Row) -> None:
        # Implementation
        ...
```

### Example 2: Programmatic Registration

```python
# User code
from iterable.plugins import register_format
from my_custom_format import MyFormatIterable

# Register at runtime
register_format("myformat", MyFormatIterable, [".mf"])

# Use immediately
from iterable.helpers.detect import open_iterable

with open_iterable("data.mf") as source:
    for row in source:
        process(row)
```

## Benefits

1. **Extensibility**: Third-party developers can extend IterableData
2. **Modularity**: Plugins are separate packages
3. **Discoverability**: Entry points enable automatic discovery
4. **Backward Compatibility**: Existing code continues to work
5. **Error Isolation**: Plugin errors don't affect core library
6. **Community Growth**: Enables ecosystem of plugins

## Challenges and Considerations

1. **Plugin Quality**: No guarantee of plugin quality
2. **Version Compatibility**: Plugins may break with library updates
3. **Security**: Plugins execute arbitrary code
4. **Performance**: Plugin discovery adds small overhead
5. **Documentation**: Need comprehensive plugin development guide

## Conclusion

A plugin system would significantly enhance IterableData's extensibility, enabling:

- **Custom formats** without modifying core library
- **Custom codecs** for new compression algorithms
- **Custom database drivers** for new database systems
- **Custom validation rules** for domain-specific validation
- **Custom engines** for new processing backends

The recommended approach uses Python's entry point system for automatic discovery, with programmatic registration as an alternative. The system maintains backward compatibility and provides error isolation to ensure plugin failures don't affect core functionality.

**Next Steps**: Implement core plugin infrastructure, integrate with existing registries, create plugin development guide.
