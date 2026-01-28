# Change: Add HTML and ARFF Format Support

## Why
Users need to process HTML tables and ARFF (Attribute-Relation File Format) files for data analysis and machine learning workflows. HTML tables are commonly found in web scraping scenarios, while ARFF is the standard format used by Weka and other machine learning tools. Currently, `iterabledata` lacks support for these formats, limiting users who work with web data or ML datasets.

## What Changes
- Add `beautifulsoup4` and `lxml` as optional dependencies for HTML parsing (lxml may already be present for XML support).
- Add `liac-arff` as an optional dependency for ARFF format support.
- Implement `HTMLIterable` in `iterable/datatypes/html.py` to extract tables from HTML files.
- Implement `ARFFIterable` in `iterable/datatypes/arff.py` to read ARFF files.
- Update `detect_file_type` to recognize `.html`, `.htm`, and `.arff` files.
- Add both iterables to `iterable/helpers/detect.py` registry.
- Add HTML and ARFF to appropriate type lists (TEXT_DATA_TYPES, FLAT_TYPES).

## Impact
- **New Capabilities**: `html-format`, `arff-format`
- **Affected Files**:
  - `pyproject.toml` (dependencies)
  - `iterable/helpers/detect.py` (format detection and registry)
  - `iterable/datatypes/html.py` (new file)
  - `iterable/datatypes/arff.py` (new file)
  - `tests/test_html.py` (new test file)
  - `tests/test_arff.py` (new test file)
  - `README.md` (documentation updates)
