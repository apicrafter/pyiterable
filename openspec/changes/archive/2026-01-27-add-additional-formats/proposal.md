# Change: Add Support for NetCDF, MVT, TopoJSON, Atom/RSS, and DXF

## Why
Users need to process a wider range of data formats, specifically in scientific (NetCDF), geospatial (MVT, TopoJSON), web feed (Atom, RSS), and CAD (DXF) domains. Adding support for these formats significantly expands the utility of `iterabledata` for diverse ETL pipelines and data analysis tasks.

## What Changes
-   **Dependencies**:
    -   Add `netCDF4` for NetCDF support.
    -   Add `mapbox-vector-tile` for MVT support.
    -   Add `topojson` for TopoJSON support.
    -   Add `feedparser` for Atom and RSS support.
    -   Add `ezdxf` for DXF support.
    -   Update `pyproject.toml` to include these as optional dependencies (extras).
-   **New Iterables**:
    -   `iterable/datatypes/netcdf.py`: Implement `NetCDFIterable`.
    -   `iterable/datatypes/mvt.py`: Implement `MVTIterable`.
    -   `iterable/datatypes/topojson.py`: Implement `TopoJSONIterable`.
    -   `iterable/datatypes/feed.py`: Implement `FeedIterable` (handling both Atom and RSS).
    -   `iterable/datatypes/dxf.py`: Implement `DXFIterable`.
-   **Detection**:
    -   Update `iterable/helpers/detect.py` to recognize extensions: `.nc`, `.mvt`, `.pbf` (context dependent), `.topojson`, `.atom`, `.rss`, `.xml` (with content checks for feeds), `.dxf`.

## Impact
-   **New Capabilities**:
    -   `netcdf-format`
    -   `mvt-format` (Mapbox Vector Tiles)
    -   `topojson-format`
    -   `feed-format` (Atom / RSS)
    -   `dxf-format`
-   **Affected Files**:
    -   `pyproject.toml`
    -   `iterable/helpers/detect.py`
    -   `iterable/datatypes/netcdf.py` (new)
    -   `iterable/datatypes/mvt.py` (new)
    -   `iterable/datatypes/topojson.py` (new)
    -   `iterable/datatypes/feed.py` (new)
    -   `iterable/datatypes/dxf.py` (new)
