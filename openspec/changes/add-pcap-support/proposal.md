# Change: Add PCAP Support

## Why
Users dealing with network traffic analysis need to process PCAP (Packet Capture) files. Currently, `iterabledata` supports many formats but lacks support for network packet logs. Adding PCAP support allows users to stream packet data row-by-row, enabling ETL pipelines for network security and monitoring data.

## What Changes
-   Add `dpkt` as an optional dependency in `pyproject.toml`.
-   Implement `PCAPIterable` in `iterable/datatypes/pcap.py`.
-   Update `detect_file_type` to recognize `.pcap` and `.pcapng` files.
-   Add `PCAPIterable` to `iterable/helpers/detect.py`.

## Impact
-   **New Capability**: `pcap-format`
-   **Affected Files**:
    -   `pyproject.toml` (dependencies)
    -   `iterable/helpers/detect.py` (formatting detection)
    -   `iterable/datatypes/pcap.py` (new file)
