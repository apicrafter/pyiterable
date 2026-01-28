## 1. Implementation
- [x] 1.1 Add `beautifulsoup4` and `liac-arff` to `project.optional-dependencies` in `pyproject.toml`
- [x] 1.2 Create `iterable/datatypes/html.py` with `HTMLIterable` class using BeautifulSoup4 for table extraction
- [x] 1.3 Create `iterable/datatypes/arff.py` with `ARFFIterable` class using `liac-arff` library
- [x] 1.4 Register `HTMLIterable` and `ARFFIterable` in `iterable/helpers/detect.py` (add to DATATYPE_REGISTRY)
- [x] 1.5 Add `html`, `htm`, and `arff` extensions to appropriate type lists (TEXT_DATA_TYPES, FLAT_TYPES) in `detect.py`
- [x] 1.6 Add `html` and `arff` extras to `all` group in `pyproject.toml` (if applicable)
- [x] 1.7 Create comprehensive tests in `tests/test_html.py` covering table extraction, multiple tables, and edge cases
- [x] 1.8 Create comprehensive tests in `tests/test_arff.py` covering standard ARFF files, sparse format, and attribute parsing
- [x] 1.9 Update `README.md` to document HTML and ARFF format support
