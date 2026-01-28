# Memory Anti-Pattern Audit: Formats Using `fobj.read()`

This document audits formats that use `fobj.read()` to load entire files into memory.

## Summary

**Total formats using `fobj.read()`**: ~25 formats
**Formats that legitimately need full file**: ~20 formats
**Formats that could potentially be streamed**: ~5 formats

## Formats Using `fobj.read()` (Full File Loading)

### Formats That Legitimately Need Full File Parsing

These formats require full file parsing due to their structure or library requirements:

1. **feed.py** - Feed formats (RSS/Atom)
   - Uses `feedparser.parse()` which requires full content
   - **Status**: Legitimate - feed parsing requires full document
   - **Streaming**: Not supported

2. **arff.py** - ARFF (Attribute-Relation File Format)
   - Uses `arff.loads()` which requires full content
   - **Status**: Legitimate - ARFF has header section that must be parsed first
   - **Streaming**: Not supported

3. **html.py** - HTML table extraction
   - Uses `BeautifulSoup()` which requires full content
   - **Status**: Legitimate - HTML parsing requires full document structure
   - **Streaming**: Not supported

4. **toml.py** - TOML format
   - Uses `tomli.loads()` or `toml.loads()` which require full content
   - **Status**: Legitimate - TOML parsing requires full document
   - **Streaming**: Not supported

5. **hocon.py** - HOCON format
   - Uses `pyhocon` which requires full content
   - **Status**: Legitimate - HOCON parsing requires full document
   - **Streaming**: Not supported

6. **edn.py** - EDN (Extensible Data Notation)
   - Uses `edn_format` which requires full content
   - **Status**: Legitimate - EDN parsing requires full document
   - **Streaming**: Not supported

7. **bencode.py** - Bencode format
   - Uses `bencode` library which requires full content
   - **Status**: Legitimate - Bencode parsing requires full document
   - **Streaming**: Not supported

8. **asn1.py** - ASN.1 format
   - Uses ASN.1 parser which requires full content
   - **Status**: Legitimate - ASN.1 parsing requires full document
   - **Streaming**: Not supported

9. **ical.py** - iCal format
   - Uses `icalendar` which requires full content
   - **Status**: Legitimate - iCal parsing requires full document structure
   - **Streaming**: Not supported

10. **turtle.py** - Turtle RDF format
    - Uses RDF parser which requires full content
    - **Status**: Legitimate - RDF parsing requires full document
    - **Streaming**: Not supported

11. **vcf.py** - VCF (Variant Call Format)
    - Uses VCF parser which requires full content
    - **Status**: Legitimate - VCF parsing requires header section
    - **Streaming**: Not supported

12. **mhtml.py** - MHTML format
    - Uses MHTML parser which requires full content
    - **Status**: Legitimate - MHTML parsing requires full document
    - **Streaming**: Not supported

13. **flexbuffers.py** - FlexBuffers format
    - Uses FlexBuffers library which requires full content
    - **Status**: Legitimate - FlexBuffers parsing requires full document
    - **Streaming**: Not supported

14. **px.py** - PC-Axis format
    - Uses custom parser which requires full content
    - **Status**: Legitimate - PC-Axis has metadata section that must be parsed first
    - **Streaming**: Not supported

15. **mvt.py** - Mapbox Vector Tile
    - Reads entire tile data
    - **Status**: Legitimate - MVT tiles are typically small binary files
    - **Streaming**: Not applicable (single tile per file)

### Formats That Could Potentially Be Streamed

These formats might benefit from streaming implementations:

1. **jsonld.py** - JSON-LD format
   - Currently reads full file, but has line-by-line detection
   - **Status**: Partially streaming - detects line-by-line format
   - **Potential**: Could improve streaming for large files
   - **Note**: Already has some streaming logic for line-by-line format

2. **ion.py** - Amazon Ion format
   - Uses `ion.loads()` which requires full content
   - **Status**: Could potentially stream - Ion supports streaming
   - **Potential**: Use `ion.load()` with file object instead of `loads()`
   - **Priority**: Medium

3. **smile.py** - SMILE (Binary JSON) format
   - Uses SMILE parser which requires full content
   - **Status**: Could potentially stream - SMILE supports streaming
   - **Potential**: Investigate streaming SMILE parser
   - **Priority**: Low

4. **ubjson.py** - UBJSON format
   - Uses UBJSON parser which requires full content
   - **Status**: Could potentially stream - UBJSON supports streaming
   - **Potential**: Investigate streaming UBJSON parser
   - **Priority**: Low

5. **jsonld.py** - Already partially addressed
   - Has line-by-line detection
   - Full document mode still loads entire file
   - **Status**: Could improve for large JSON-LD documents
   - **Priority**: Low

## Formats Using `fobj.read(n)` (Size-Limited Reads)

These formats use `fobj.read(n)` with size arguments, which is acceptable:

- **tfrecord.py** - Reads fixed-size headers
- **sequencefile.py** - Reads fixed-size headers
- **recordio.py** - Reads fixed-size headers
- **protobuf.py** - Reads size-prefixed messages
- **kafka.py** - Reads size-prefixed messages
- **pulsar.py** - Reads size-prefixed messages
- **beam.py** - Reads size-prefixed messages
- **flink.py** - Reads size-prefixed messages
- **cbor.py** - Reads size-prefixed data
- **capnp.py** - Reads size-prefixed data

**Status**: These are fine - they read in chunks, not entire files.

## Recommendations

1. **Ensure non-streaming formats are properly marked**:
   - All formats using `fobj.read()` should have `is_streaming()` return `False`
   - Update capability system to reflect accurate streaming status

2. **Consider streaming for Ion format** (Medium priority):
   - Investigate using `ion.load()` with file object for streaming

3. **Document memory implications**:
   - Add warnings in documentation for formats that load entire files
   - Document file size recommendations

4. **No immediate fixes needed** for most formats:
   - Most formats legitimately require full file parsing
   - Focus should be on proper documentation and capability marking

## Action Items

- [x] Audit all formats using `fobj.read()`
- [ ] Ensure all non-streaming formats have `is_streaming() == False`
- [ ] Update capability system to reflect accurate streaming status
- [ ] Add memory warnings in documentation
- [ ] Consider streaming implementation for Ion format (optional)
