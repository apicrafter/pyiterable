## ADDED Requirements

### Requirement: PCAP File Reading
The system SHALL support reading PCAP (Packet Capture) files and yielding packets as dictionary records.

#### Scenario: Read standard PCAP
- **WHEN** opening a valid `.pcap` file
- **THEN** it yields records containing timestamp and packet data

#### Scenario: Read PCAP with automatic detection
- **WHEN** using `open_iterable` on a `.pcap` file
- **THEN** it automatically selects `PCAPIterable`

#### Scenario: Handle missing dependency
- **WHEN** `dpkt` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[pcap]`
