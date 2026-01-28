## 1. HTML Format Implementation
- [x] 1.1 Implement `has_tables()` static method in `HTMLIterable` (returns `True`)
- [x] 1.2 Implement `list_tables()` instance method in `HTMLIterable` (parse HTML, find all `<table>` elements, return indices or IDs/names)
- [x] 1.3 Implement `list_tables()` class method in `HTMLIterable` (open file temporarily, parse, return table list)
- [x] 1.4 Handle edge cases: empty HTML, no tables, tables with/without IDs or captions

## 2. XML Format Implementation
- [x] 2.1 Implement `has_tables()` static method in `XMLIterable` (returns `True`)
- [x] 2.2 Implement `list_tables()` instance method in `XMLIterable` (parse XML, find all unique tag names, return list)
- [x] 2.3 Implement `list_tables()` class method in `XMLIterable` (open file temporarily, parse, return tag names)
- [x] 2.4 Handle edge cases: empty XML, no elements, namespaced tags

## 3. ZIPXML Format Implementation
- [x] 3.1 Implement `has_tables()` static method in `ZIPXMLSource` (returns `True`)
- [x] 3.2 Implement `list_tables()` instance method in `ZIPXMLSource` (list all XML files in ZIP archive)
- [x] 3.3 Implement `list_tables()` class method in `ZIPXMLSource` (open ZIP temporarily, return file list)
- [x] 3.4 Handle edge cases: empty ZIP, no XML files, non-XML files in archive

## 4. Iceberg Format Implementation
- [x] 4.1 Implement `has_tables()` static method in `IcebergIterable` (returns `True`)
- [x] 4.2 Implement `list_tables()` instance method in `IcebergIterable` (list all tables in catalog)
- [x] 4.3 Implement `list_tables()` class method in `IcebergIterable` (connect to catalog, return table names)
- [x] 4.4 Handle edge cases: empty catalog, missing catalog configuration, connection errors

## 5. Hudi Format Implementation
- [x] 5.1 Implement `has_tables()` static method in `HudiIterable` (returns `True`)
- [x] 5.2 Implement `list_tables()` instance method in `HudiIterable` (list all tables in catalog or directory)
- [x] 5.3 Implement `list_tables()` class method in `HudiIterable` (connect to catalog/directory, return table names)
- [x] 5.4 Handle edge cases: empty catalog/directory, missing configuration, connection errors

## 6. Delta Format Implementation
- [x] 6.1 Implement `has_tables()` static method in `DeltaIterable` (returns `True` if catalog-based, `False` if single table)
- [x] 6.2 Implement `list_tables()` instance method in `DeltaIterable` (list all tables in catalog/directory if applicable)
- [x] 6.3 Implement `list_tables()` class method in `DeltaIterable` (connect to catalog/directory, return table names)
- [x] 6.4 Handle edge cases: single table directory (return `None` or empty list), empty catalog, connection errors

## 7. Testing
- [x] 7.1 Add tests for `list_tables()` in `test_html.py` (both class and instance methods, multiple tables, table IDs)
- [x] 7.2 Add tests for `list_tables()` in `test_xml.py` (both class and instance methods, multiple tag names)
- [x] 7.3 Add tests for `list_tables()` in `test_zipxml.py` (both class and instance methods, multiple XML files)
- [x] 7.4 Add tests for `list_tables()` in `test_iceberg.py` (both class and instance methods, catalog tables)
- [x] 7.5 Add tests for `list_tables()` in `test_hudi.py` (both class and instance methods, catalog/directory tables)
- [x] 7.6 Add tests for `list_tables()` in `test_delta.py` (both class and instance methods, catalog/directory tables)
- [x] 7.7 Add tests for edge cases: empty files, missing dependencies, invalid files
- [x] 7.8 Add tests for `has_tables()` static method for all new formats

## 8. Documentation
- [x] 8.1 Update `docs/docs/formats/html.md` with table listing examples
- [x] 8.2 Update `docs/docs/formats/xml.md` with table listing examples
- [x] 8.3 Update `docs/docs/formats/zipxml.md` with table listing examples
- [x] 8.4 Update `docs/docs/formats/iceberg.md` with table listing examples
- [x] 8.5 Update `docs/docs/formats/hudi.md` with table listing examples
- [x] 8.6 Update `docs/docs/formats/delta.md` with table listing examples
- [x] 8.7 Update `docs/docs/api/base-iterable.md` to include new formats in supported formats list
- [x] 8.8 Update `CHANGELOG.md` with extended table listing feature
