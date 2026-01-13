## 1. Base Interface
- [x] 1.1 Add `has_tables()` static method to `BaseIterable` (returns `False` by default)
- [x] 1.2 Add `list_tables()` instance method to `BaseIterable` (returns `None` by default, indicating not supported)
- [x] 1.3 Add `list_tables()` class method signature to `BaseIterable` (takes filename, returns `None` by default)
- [x] 1.4 Update `BaseFileIterable` if needed for common implementation patterns

## 2. Excel Format Implementations
- [x] 2.1 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `XLSXIterable` (return sheet names, reuse workbook if open)
- [x] 2.2 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `XLSIterable` (return sheet names, reuse workbook if open)
- [x] 2.3 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `ODSIterable` (return sheet names, reuse document if open)

## 3. Database Format Implementations
- [x] 3.1 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `SQLiteIterable` (return table names, reuse connection if open)
- [x] 3.2 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `DuckDBDatabaseIterable` (return table names, reuse connection if open)

## 4. Scientific Format Implementations
- [x] 4.1 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `HDF5Iterable` (return dataset paths, reuse file handle if open)
- [x] 4.2 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `NetCDFIterable` (return variable names, reuse dataset if open)

## 5. Geospatial Format Implementations
- [x] 5.1 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `GeoPackageIterable` (return layer names, reuse collection if open)

## 6. Statistical Format Implementations
- [x] 6.1 Implement `has_tables()` and `list_tables()` (both class and instance methods) in `RDataIterable` (return R object names)

## 7. Testing
- [x] 7.1 Add tests for `list_tables()` class method in `test_xlsx.py` (multiple sheets, without opening)
- [x] 7.2 Add tests for `list_tables()` instance method in `test_xlsx.py` (on already-opened file, reuse workbook)
- [ ] 7.3 Add tests for `list_tables()` in `test_xls.py` (both class and instance methods)
- [ ] 7.4 Add tests for `list_tables()` in `test_ods.py` (both class and instance methods)
- [x] 7.5 Add tests for `list_tables()` in `test_sqlite.py` (both class and instance methods, connection reuse)
- [ ] 7.6 Add tests for `list_tables()` in `test_duckdb_format.py` (both class and instance methods, connection reuse)
- [ ] 7.7 Add tests for `list_tables()` in `test_hdf5.py` (both class and instance methods)
- [ ] 7.8 Add tests for `list_tables()` in `test_netcdf.py` (both class and instance methods)
- [ ] 7.9 Add tests for `list_tables()` in `test_geopackage.py` (both class and instance methods)
- [ ] 7.10 Add tests for `list_tables()` in `test_rdata.py` (both class and instance methods)
- [ ] 7.11 Add tests for formats that don't support tables (should return `None`)
- [x] 7.12 Add tests for `has_tables()` static method across all formats
- [x] 7.13 Add tests for empty files/databases (should return `[]`)
- [ ] 7.14 Add tests for edge cases (missing dependencies, invalid files)

## 8. Documentation
- [x] 8.1 Update `docs/docs/api/base-iterable.md` with `list_tables()` and `has_tables()` documentation (both class and instance methods)
- [x] 8.2 Update format-specific docs (xlsx.md, xls.md, ods.md, sqlite.md, duckdb.md, hdf5.md, geopackage.md, rdata.md) with table listing examples
- [x] 8.3 Add usage examples showing both discovery patterns (before and after opening)
- [x] 8.4 Update `CHANGELOG.md` with table listing feature
