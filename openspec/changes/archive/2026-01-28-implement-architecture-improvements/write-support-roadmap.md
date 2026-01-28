# Write Support Implementation Roadmap

This document outlines the implementation roadmap for adding write support to currently read-only formats in IterableData.

**Last Updated**: 2026-01-27  
**Total Read-Only Formats**: 27  
**Formats with Write Support**: 67

## Overview

Based on the write implementation audit (see `dev/write_implementation_audit.txt`), there are 27 formats that currently do not support write operations. This roadmap categorizes these formats by priority and implementation feasibility, providing a structured plan for adding write support.

## Priority Categories

### Priority 1: High Value, Feasible (Recommended for Next Release)

These formats have clear use cases, existing Python libraries with write support, and are relatively straightforward to implement.

#### Formats:
1. **Avro** (`.avro`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `avro-python3` (already used for reading)
   - **Complexity**: Medium
   - **Use Case**: Data serialization, Hadoop ecosystem
   - **Estimated Effort**: 2-3 days
   - **Dependencies**: `avro-python3` (already required)

2. **XML** (`.xml`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `lxml` (already used for reading)
   - **Complexity**: Medium
   - **Use Case**: Document processing, data exchange
   - **Estimated Effort**: 2-3 days
   - **Dependencies**: `lxml` (already required)
   - **Note**: Need to handle XML structure preservation, namespaces, attributes

3. **XLS** (`.xls`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `xlwt` or `pyexcel-xls`
   - **Complexity**: Medium
   - **Use Case**: Legacy Excel file support
   - **Estimated Effort**: 2-3 days
   - **Dependencies**: `xlwt` or `pyexcel-xls` (new dependency)
   - **Note**: XLSX already has write support; XLS is legacy format

4. **PSV** (`.psv`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: Similar to CSV (can reuse CSV writer)
   - **Complexity**: Low
   - **Use Case**: Pipe-separated values (common in Unix/Linux)
   - **Estimated Effort**: 1 day
   - **Dependencies**: None (can reuse CSV implementation)
   - **Note**: Very similar to CSV, just different delimiter

5. **DBF** (`.dbf`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `dbfread` (read-only) or `dbfpy3`/`dbf` for writing
   - **Complexity**: Medium
   - **Use Case**: Legacy database files, shapefile support
   - **Estimated Effort**: 2-3 days
   - **Dependencies**: `dbfpy3` or `dbf` (new dependency)
   - **Note**: Used by shapefile format (which already has write support)

### Priority 2: Medium Value, Moderate Complexity

These formats have use cases but may require more effort or have limited library support.

#### Formats:
6. **ODS** (`.ods`)
   - **Status**: Explicitly raises `WriteNotSupportedError`
   - **Library**: `odfpy` or `pyexcel-ods3`
   - **Complexity**: Medium-High
   - **Use Case**: OpenDocument Spreadsheet format
   - **Estimated Effort**: 3-4 days
   - **Dependencies**: `odfpy` or `pyexcel-ods3` (may already be available)
   - **Note**: Similar to Excel but different format structure

7. **NetCDF** (`.nc`, `.netcdf`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `netCDF4` or `scipy.io.netcdf`
   - **Complexity**: High
   - **Use Case**: Scientific data, climate data
   - **Estimated Effort**: 4-5 days
   - **Dependencies**: `netCDF4` (new dependency)
   - **Note**: Complex format with dimensions, variables, attributes

8. **MVT** (`.mvt`, `.pbf`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `mapbox-vector-tile` or `protobuf` (for encoding)
   - **Complexity**: Medium-High
   - **Use Case**: Mapbox Vector Tiles, geospatial data
   - **Estimated Effort**: 3-4 days
   - **Dependencies**: `mapbox-vector-tile` or `protobuf` (may already be available)
   - **Note**: Binary format, requires protobuf encoding

9. **DXF** (`.dxf`)
   - **Status**: Base class default (not yet implemented)
   - **Library**: `ezdxf`
   - **Complexity**: High
   - **Use Case**: CAD drawings, engineering
   - **Estimated Effort**: 4-5 days
   - **Dependencies**: `ezdxf` (new dependency)
   - **Note**: Complex CAD format with many entity types

### Priority 3: Lower Priority or Specialized

These formats have limited use cases, are very complex, or have better alternatives.

#### Formats:
10. **Zipped** (`.zipped`)
    - **Status**: Base class default (not yet implemented)
    - **Complexity**: Low-Medium
    - **Use Case**: Generic zip container
    - **Estimated Effort**: 2-3 days
    - **Note**: Generic format, may not be high priority

11. **ZipXML** (`.zipxml`)
    - **Status**: Base class default (not yet implemented)
    - **Complexity**: Medium
    - **Use Case**: XML in zip container (e.g., Office formats)
    - **Estimated Effort**: 2-3 days
    - **Note**: Combination of zip and XML handling

### Priority 4: Statistical/Proprietary Formats (Low Priority)

These formats are primarily read-only in practice and have limited write use cases.

#### Formats:
12. **ARFF** (`.arff`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: Custom implementation or `scipy.io.arff` (read-only)
    - **Complexity**: Low-Medium
    - **Use Case**: Machine learning datasets (Weka format)
    - **Estimated Effort**: 2-3 days
    - **Note**: Text-based format, relatively simple structure

13. **SAS** (`.sas`, `.sas7bdat`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `sas7bdat` (read-only) or `pyreadstat` (limited write)
    - **Complexity**: High
    - **Use Case**: Statistical analysis (SAS format)
    - **Estimated Effort**: 5-7 days
    - **Note**: Proprietary format, complex structure, limited library support

14. **SPSS** (`.sav`, `.spss`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyreadstat` (has write support)
    - **Complexity**: Medium-High
    - **Use Case**: Statistical analysis (SPSS format)
    - **Estimated Effort**: 3-4 days
    - **Dependencies**: `pyreadstat` (may already be available)
    - **Note**: `pyreadstat` supports writing SPSS files

15. **Stata** (`.dta`, `.stata`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyreadstat` (has write support)
    - **Complexity**: Medium
    - **Use Case**: Statistical analysis (Stata format)
    - **Estimated Effort**: 3-4 days
    - **Dependencies**: `pyreadstat` (may already be available)
    - **Note**: `pyreadstat` supports writing Stata files

16. **RData** (`.rdata`, `.rda`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyreadr` (read-only) or `rpy2` (requires R)
    - **Complexity**: High
    - **Use Case**: R statistical data format
    - **Estimated Effort**: 5-7 days
    - **Note**: Requires R or complex serialization

17. **RDS** (`.rds`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyreadr` (read-only) or `rpy2` (requires R)
    - **Complexity**: High
    - **Use Case**: R single object serialization
    - **Estimated Effort**: 5-7 days
    - **Note**: Requires R or complex serialization

18. **PC-Axis (PX)** (`.px`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: Custom implementation
    - **Complexity**: Medium
    - **Use Case**: Statistical data exchange (European standard)
    - **Estimated Effort**: 3-4 days
    - **Note**: Text-based format, relatively simple

### Priority 5: Columnar Storage Formats (Engine-Managed)

These formats are typically managed through their respective engines rather than direct file writing.

#### Formats:
19. **Delta Lake**
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `deltalake` (has write support)
    - **Complexity**: High
    - **Use Case**: Data lake storage, ACID transactions
    - **Estimated Effort**: 5-7 days
    - **Dependencies**: `deltalake` (already required)
    - **Note**: Typically managed through Spark/PySpark, but direct write is possible

20. **Apache Iceberg**
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyiceberg` (has write support)
    - **Complexity**: High
    - **Use Case**: Data lake storage, table format
    - **Estimated Effort**: 5-7 days
    - **Dependencies**: `pyiceberg` (already required)
    - **Note**: Typically managed through engines, but direct write is possible

21. **Apache Hudi**
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `pyhudi` or `hudi` (has write support)
    - **Complexity**: High
    - **Use Case**: Data lake storage, incremental processing
    - **Estimated Effort**: 5-7 days
    - **Dependencies**: `pyhudi` or `hudi` (already required)
    - **Note**: Typically managed through engines, but direct write is possible

### Priority 6: Specialized Formats (Very Low Priority)

These formats have very specific use cases and may not benefit significantly from write support.

#### Formats:
22. **PCAP** (`.pcap`, `.pcapng`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `dpkt` (read-only) or `pcap` library
    - **Complexity**: Medium-High
    - **Use Case**: Network packet capture
    - **Estimated Effort**: 3-4 days
    - **Note**: Typically generated by network tools, not programmatically

23. **HTML** (`.html`, `.htm`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `lxml` or `html5lib`
    - **Complexity**: Medium
    - **Use Case**: HTML document generation
    - **Estimated Effort**: 2-3 days
    - **Note**: HTML writing is typically done with templating libraries

24. **Feed** (`.atom`, `.rss`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `feedparser` (read-only) or custom implementation
    - **Complexity**: Low-Medium
    - **Use Case**: RSS/Atom feed generation
    - **Estimated Effort**: 2-3 days
    - **Note**: XML-based format, relatively simple

25. **FlatBuffers** (`.fbs`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `flatbuffers` (has write support)
    - **Complexity**: Medium-High
    - **Use Case**: Serialization format
    - **Estimated Effort**: 3-4 days
    - **Dependencies**: `flatbuffers` (already required)
    - **Note**: Requires schema definition

26. **HDF5** (`.hdf5`, `.h5`)
    - **Status**: Explicitly raises `WriteNotSupportedError`
    - **Library**: `h5py` (has write support)
    - **Complexity**: High
    - **Use Case**: Scientific data storage
    - **Estimated Effort**: 5-7 days
    - **Dependencies**: `h5py` (already required)
    - **Note**: Complex format with groups, datasets, attributes

## Implementation Phases

### Phase 1: Quick Wins (1-2 weeks)
Focus on formats with low complexity and high value:
- PSV (1 day)
- Avro (2-3 days)
- XML (2-3 days)
- XLS (2-3 days)
- DBF (2-3 days)

**Total Estimated Effort**: 9-13 days

### Phase 2: Medium Priority (2-3 weeks)
Focus on formats with moderate complexity:
- ODS (3-4 days)
- MVT (3-4 days)
- ARFF (2-3 days)
- PC-Axis (3-4 days)
- HTML (2-3 days)
- Feed (2-3 days)

**Total Estimated Effort**: 15-21 days

### Phase 3: Statistical Formats (2-3 weeks)
Focus on statistical formats with existing library support:
- SPSS (3-4 days) - using `pyreadstat`
- Stata (3-4 days) - using `pyreadstat`
- NetCDF (4-5 days)

**Total Estimated Effort**: 10-13 days

### Phase 4: Complex Formats (3-4 weeks)
Focus on complex formats requiring significant effort:
- DXF (4-5 days)
- HDF5 (5-7 days)
- Delta Lake (5-7 days)
- Iceberg (5-7 days)
- Hudi (5-7 days)
- RData/RDS (5-7 days each, may skip)

**Total Estimated Effort**: 29-38 days

### Phase 5: Specialized Formats (1-2 weeks)
Focus on specialized formats with limited use cases:
- PCAP (3-4 days)
- FlatBuffers (3-4 days)
- Zipped/ZipXML (2-3 days each)
- SAS (5-7 days, low priority)

**Total Estimated Effort**: 13-18 days

## Recommendations

### Immediate Actions (Next Release)
1. **Implement Priority 1 formats** (Avro, XML, XLS, PSV, DBF)
   - High value, feasible, clear use cases
   - Estimated: 1-2 weeks

2. **Update documentation** to reflect new write support
3. **Add tests** for all new write implementations
4. **Update capability system** to reflect new write support

### Medium-Term (Next 2-3 Releases)
1. **Implement Priority 2 formats** (ODS, NetCDF, MVT, DXF)
2. **Implement statistical formats** (SPSS, Stata) using `pyreadstat`
3. **Consider columnar storage formats** (Delta, Iceberg, Hudi) if there's user demand

### Long-Term (Future Releases)
1. **Evaluate user demand** for remaining formats
2. **Consider deprecating** formats with very low usage
3. **Focus on formats** with active community requests

## Implementation Guidelines

### For Each Format Implementation:

1. **Research existing libraries**
   - Check if library already supports writing
   - Evaluate library quality and maintenance status
   - Consider license compatibility

2. **Design write interface**
   - Follow existing patterns in IterableData
   - Support both `write()` and `write_bulk()`
   - Handle format-specific options via `iterableargs`

3. **Implement write methods**
   - Start with basic write support
   - Add format-specific features incrementally
   - Ensure compatibility with read implementation

4. **Add tests**
   - Test basic write operations
   - Test write_bulk operations
   - Test round-trip (write then read)
   - Test error handling

5. **Update documentation**
   - Update format-specific documentation
   - Update capability matrix
   - Add examples

6. **Update capability system**
   - Remove format from `READ_ONLY_FORMATS`
   - Verify capability detection works correctly

## Success Metrics

- **Format Coverage**: Increase write support from 67 to 85+ formats (70%+ coverage)
- **User Satisfaction**: Reduce requests for write support
- **Code Quality**: Maintain test coverage >80% for new implementations
- **Documentation**: Keep documentation up-to-date with new capabilities

## Notes

- Some formats (like SAS, RData, RDS) may require significant effort and have limited use cases
- Columnar storage formats (Delta, Iceberg, Hudi) are typically managed through engines, but direct write support may be valuable
- Statistical formats (SPSS, Stata) have existing library support via `pyreadstat`
- Some formats may be better served by conversion workflows rather than direct write support

## Tracking

This roadmap should be updated as formats are implemented. Track progress in:
- `openspec/changes/implement-architecture-improvements/tasks.md`
- Format-specific documentation
- Capability system updates
- CHANGELOG.md entries
