# Suggested File Formats to Add

This document lists iterable data file formats that could be added to the pyiterable repository. Formats are categorized by use case and include a brief description of why they would be valuable additions.

## Log Formats

### 1. **LTSV (Labeled Tab-Separated Values)**
- **Extensions**: `.ltsv`
- **Type**: Text, line-based
- **Description**: Each line contains key-value pairs separated by tabs. Format: `key1:value1\tkey2:value2\n`
- **Use Case**: Structured logging, especially in Japanese web services
- **Example**: `time:2023-01-01T00:00:00Z\thost:example.com\tstatus:200\n`
- **Complexity**: Low - Similar to TSV but with key-value semantics

### 2. **Logfmt**
- **Extensions**: `.logfmt`
- **Type**: Text, line-based
- **Description**: Structured logging format with key=value pairs separated by spaces
- **Use Case**: Modern structured logging (used by Heroku, Docker, etc.)
- **Example**: `time=2023-01-01T00:00:00Z host=example.com status=200 method=GET`
- **Complexity**: Low - Simple key=value parsing with quoted string support

### 3. **Syslog**
- **Extensions**: `.syslog`, `.log` (when syslog format)
- **Type**: Text, line-based
- **Description**: Standard system logging format (RFC 3164/5424)
- **Use Case**: System logs, network device logs
- **Example**: `<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8`
- **Complexity**: Medium - Requires parsing structured header and message

### 4. **Nginx Access Log**
- **Extensions**: `.nginx.log`, `.access.log` (when nginx format)
- **Type**: Text, line-based
- **Description**: Nginx web server access log format (configurable but has common patterns)
- **Use Case**: Web server log analysis
- **Example**: `127.0.0.1 - - [25/Dec/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"`
- **Complexity**: Medium - Similar to Apache log but different format

### 5. **IIS Log Format**
- **Extensions**: `.iis.log`, `.w3c.log`
- **Type**: Text, line-based
- **Description**: Microsoft IIS web server log format (W3C Extended Log Format)
- **Use Case**: Windows web server log analysis
- **Example**: `#Fields: date time s-ip cs-method cs-uri-stem sc-status cs-version\n2023-01-01 00:00:00 192.168.1.1 GET /index.html 200 HTTP/1.1`
- **Complexity**: Medium - Header-based format with configurable fields

### 6. **Apache Log4j Format**
- **Extensions**: `.log4j`, `.log` (when log4j format)
- **Type**: Text, line-based
- **Description**: Java Log4j logging format (pattern-based)
- **Use Case**: Java application logs
- **Example**: `2023-01-01 00:00:00,000 INFO [main] com.example.App - Application started`
- **Complexity**: Medium - Pattern-based format requires configuration

## Web/HTTP Formats

### 7. **HAR (HTTP Archive)**
- **Extensions**: `.har`
- **Type**: Text (JSON-based), record-based
- **Description**: Format for exporting HTTP transactions from browsers
- **Use Case**: Web performance analysis, debugging web applications
- **Complexity**: Medium - JSON structure with nested entries array
- **Note**: Each entry in the `log.entries` array is a record

### 8. **PCAP (Packet Capture)**
- **Extensions**: `.pcap`, `.cap`
- **Type**: Binary, packet-based
- **Description**: Network packet capture format
- **Use Case**: Network analysis, security monitoring
- **Complexity**: High - Requires libpcap/pypcap library
- **Note**: Each packet is a record, but requires specialized parsing

## JSON Variants

### 9. **JSON5**
- **Extensions**: `.json5`
- **Type**: Text, document-based (like JSON)
- **Description**: JSON with comments, trailing commas, and other enhancements
- **Use Case**: Configuration files, human-readable JSON
- **Example**: `{ // comment\n  name: "value", // trailing comma\n}`
- **Complexity**: Medium - Requires json5 library

### 10. **HJSON (Human JSON)**
- **Extensions**: `.hjson`
- **Type**: Text, document-based
- **Description**: Human-readable JSON with comments and relaxed syntax
- **Use Case**: Configuration files, documentation
- **Example**: `{ # comment\n  name: value\n  // another comment\n}`
- **Complexity**: Medium - Requires hjson library

### 11. **JSONC (JSON with Comments)**
- **Extensions**: `.jsonc`
- **Type**: Text, document-based
- **Description**: JSON with C-style comments (// and /* */)
- **Use Case**: Configuration files (used by VS Code, etc.)
- **Complexity**: Low - Can strip comments then parse as JSON

## Time Series Formats

### 12. **Prometheus Format**
- **Extensions**: `.prom`, `.metrics`
- **Type**: Text, line-based
- **Description**: Prometheus metrics export format
- **Use Case**: Metrics collection, monitoring data
- **Example**: `http_requests_total{method="GET",status="200"} 1234 1609459200000`
- **Complexity**: Low - Simple key-value format with labels

### 13. **Graphite Format**
- **Extensions**: `.graphite`, `.carbon`
- **Type**: Text, line-based
- **Description**: Graphite time series data format
- **Use Case**: Time series metrics, monitoring
- **Example**: `server.cpu.usage 85.5 1609459200`
- **Complexity**: Low - Simple metric path, value, timestamp format

### 14. **OpenTSDB Format**
- **Extensions**: `.opentsdb`, `.tsdb`
- **Type**: Text, line-based (JSON)
- **Description**: OpenTSDB data format (JSON per line)
- **Use Case**: Time series database exports
- **Example**: `{"metric":"sys.cpu.nice","timestamp":1609459200,"value":18,"tags":{"host":"web01","dc":"lga"}}`
- **Complexity**: Low - JSONL with specific schema

## Big Data/Streaming Formats

### 15. **Apache Spark Checkpoint Format**
- **Extensions**: `.spark`, `.checkpoint`
- **Type**: Binary, record-based
- **Description**: Apache Spark checkpoint/savepoint format
- **Use Case**: Spark job state, data processing pipelines
- **Complexity**: High - Requires Spark libraries or format specification

### 16. **Apache Storm Format**
- **Extensions**: `.storm`
- **Type**: Binary, record-based
- **Description**: Apache Storm checkpoint format
- **Use Case**: Stream processing state
- **Complexity**: High - Requires Storm libraries

### 17. **Apache Spark SQL Format**
- **Extensions**: `.spark.sql`
- **Type**: Binary/Text, depends on format
- **Description**: Spark SQL DataFrame serialization format
- **Use Case**: Spark data processing
- **Complexity**: High - Requires Spark/pyarrow

## Database Export Formats

### 18. **MongoDB Export Format**
- **Extensions**: `.mongo.json`, `.mongo.csv`
- **Type**: Text, line-based (JSON or CSV)
- **Description**: MongoDB mongoexport output format
- **Use Case**: MongoDB data exports
- **Complexity**: Low - JSONL or CSV format

### 19. **Redis RDB Format**
- **Extensions**: `.rdb`, `.redis`
- **Type**: Binary, key-value based
- **Description**: Redis database dump format
- **Use Case**: Redis backup/restore, data migration
- **Complexity**: High - Requires redis-rdb-tools or custom parser

### 20. **SQL Server BCP Format**
- **Extensions**: `.bcp`, `.sqlserver`
- **Type**: Text, row-based
- **Description**: SQL Server Bulk Copy Program format
- **Use Case**: SQL Server data exports
- **Complexity**: Medium - Similar to CSV but with specific encoding

### 21. **Oracle SQL*Loader Format**
- **Extensions**: `.dat`, `.oracle`
- **Type**: Text, row-based
- **Description**: Oracle SQL*Loader data format
- **Use Case**: Oracle database imports/exports
- **Complexity**: Medium - Fixed-width or delimited format

## Scientific/Specialized Formats

### 22. **PLINK Format**
- **Extensions**: `.ped`, `.fam`, `.map`
- **Type**: Text, row-based
- **Description**: Genetics data format (PLINK)
- **Use Case**: Genetic association studies, bioinformatics
- **Example**: `FAM001 1 0 0 1 1 1 1 2 2 1 2`
- **Complexity**: Medium - Fixed-width format with specific schema

### 23. **FASTA/FASTQ Format**
- **Extensions**: `.fasta`, `.fa`, `.fastq`, `.fq`
- **Type**: Text, sequence-based
- **Description**: Biological sequence format
- **Use Case**: Bioinformatics, genomics
- **Example**: `>sequence1\nATCGATCG\n>sequence2\nGCTAGCTA`
- **Complexity**: Low - Simple header + sequence format

### 24. **SAM/BAM Format**
- **Extensions**: `.sam`, `.bam`
- **Type**: Text (SAM) / Binary (BAM), row-based
- **Description**: Sequence Alignment/Map format
- **Use Case**: Genomics, sequence alignment
- **Complexity**: Medium - Tab-delimited with specific columns

### 25. **NetCDF Format**
- **Extensions**: `.nc`, `.netcdf`
- **Type**: Binary, array-based
- **Description**: Network Common Data Format
- **Use Case**: Scientific data, climate data, oceanography
- **Complexity**: High - Requires netCDF4 library, can iterate over variables/dimensions

### 26. **FITS Format**
- **Extensions**: `.fits`, `.fit`
- **Type**: Binary, header-data units
- **Description**: Flexible Image Transport System (astronomy)
- **Use Case**: Astronomy data, image data
- **Complexity**: High - Requires astropy or pyfits library

## Configuration/Data Formats

### 27. **Properties File Format**
- **Extensions**: `.properties`
- **Type**: Text, key-value based
- **Description**: Java properties file format
- **Use Case**: Java application configuration
- **Example**: `key1=value1\nkey2=value2\n# comment`
- **Complexity**: Low - Similar to INI but simpler
- **Note**: INI format might cover this, but Properties has specific escaping rules

### 28. **Env File Format**
- **Extensions**: `.env`
- **Type**: Text, key-value based
- **Description**: Environment variable file format
- **Use Case**: Application configuration, Docker
- **Example**: `KEY1=value1\nKEY2=value2\n# comment`
- **Complexity**: Low - Simple key=value format

### 29. **Dotenv Format**
- **Extensions**: `.env`, `.dotenv`
- **Type**: Text, key-value based
- **Description**: Environment variable format with variable expansion
- **Use Case**: Application configuration
- **Complexity**: Low - Similar to env but with variable substitution

## Other Formats

### 30. **Apache Common Log Format (CLF)**
- **Extensions**: `.clf`, `.common.log`
- **Type**: Text, line-based
- **Description**: Standard Apache common log format (simpler than combined)
- **Use Case**: Web server logs
- **Example**: `127.0.0.1 - - [25/Dec/2023:10:00:00 +0000] "GET /index.html HTTP/1.0" 200 1234`
- **Complexity**: Low - Simpler variant of Apache log
- **Note**: Apache Log format might already cover this

### 31. **Apache Combined Log Format**
- **Extensions**: `.combined.log`
- **Type**: Text, line-based
- **Description**: Apache combined log format (includes referrer and user-agent)
- **Use Case**: Web server logs
- **Complexity**: Low - Extension of common log format
- **Note**: Apache Log format might already cover this

### 32. **ELF (Executable and Linkable Format)**
- **Extensions**: `.elf`
- **Type**: Binary, section-based
- **Description**: Executable file format (Linux/Unix)
- **Use Case**: Binary analysis, reverse engineering
- **Complexity**: High - Requires specialized parsing, sections can be iterated

### 33. **Mach-O Format**
- **Extensions**: `.macho`, `.o`
- **Type**: Binary, segment-based
- **Description**: macOS/iOS executable format
- **Use Case**: Binary analysis, macOS development
- **Complexity**: High - Requires specialized parsing

### 34. **Windows Event Log Format (EVTX)**
- **Extensions**: `.evtx`, `.evt`
- **Type**: Binary, event-based
- **Description**: Windows Event Log format
- **Use Case**: Windows system logs, security auditing
- **Complexity**: High - Requires python-evtx or similar library

### 35. **Journald Format**
- **Extensions**: `.journal`, `.journald`
- **Type**: Binary, entry-based
- **Description**: systemd journal format
- **Use Case**: Linux system logs
- **Complexity**: High - Requires systemd libraries or python-systemd

### 36. **Logstash Format**
- **Extensions**: `.logstash`
- **Type**: Text (JSON), line-based
- **Description**: Logstash output format (JSON per line)
- **Use Case**: Log processing pipelines
- **Complexity**: Low - JSONL format with specific schema

### 37. **Fluentd Format**
- **Extensions**: `.fluentd`, `.msgpack` (when used by Fluentd)
- **Type**: Binary (MessagePack), record-based
- **Description**: Fluentd log forwarding format
- **Use Case**: Log aggregation, log forwarding
- **Complexity**: Medium - MessagePack with Fluentd-specific tags

### 38. **Graylog Format**
- **Extensions**: `.graylog`, `.gelf` (GELF variant)
- **Type**: Text (JSON), line-based
- **Description**: Graylog log format (GELF or JSON)
- **Use Case**: Centralized logging
- **Complexity**: Low - JSONL or GELF format

### 39. **Splunk Format**
- **Extensions**: `.splunk`, `.spl`
- **Type**: Text, line-based
- **Description**: Splunk search results export format
- **Use Case**: Log analysis, SIEM
- **Complexity**: Medium - CSV-like format with metadata

### 40. **ELK Stack Format (Elasticsearch)**
- **Extensions**: `.elk`, `.elasticsearch`
- **Type**: Text (JSON), line-based
- **Description**: Elasticsearch bulk API format (NDJSON)
- **Use Case**: Elasticsearch data exports
- **Complexity**: Low - JSONL with action/metadata lines

## Additional Web/HTTP Formats

### 41. **CURL Format**
- **Extensions**: `.curl`, `.http`
- **Type**: Text, request-based
- **Description**: HTTP request format (curl commands or HTTP/1.1)
- **Use Case**: API testing, HTTP debugging
- **Complexity**: Medium - HTTP request parsing

### 42. **HTTP Archive v2 (HAR2)**
- **Extensions**: `.har2`
- **Type**: Text (JSON), record-based
- **Description**: Enhanced HAR format with additional metadata
- **Use Case**: Web performance analysis
- **Complexity**: Medium - JSON structure similar to HAR

### 43. **WebVTT (Web Video Text Tracks)**
- **Extensions**: `.vtt`
- **Type**: Text, cue-based
- **Description**: Web video subtitle/caption format
- **Use Case**: Video subtitles, timed text
- **Example**: `WEBVTT\n\n00:00:01.000 --> 00:00:04.000\nHello world`
- **Complexity**: Low - Simple timestamped text format

### 44. **SRT (SubRip Subtitle)**
- **Extensions**: `.srt`
- **Type**: Text, subtitle-based
- **Description**: Subtitle format with sequence numbers
- **Use Case**: Video subtitles
- **Example**: `1\n00:00:01,000 --> 00:00:04,000\nHello world\n\n`
- **Complexity**: Low - Sequential subtitle blocks

### 45. **Sitemap XML**
- **Extensions**: `.sitemap`, `.sitemap.xml`
- **Type**: Text (XML), URL-based
- **Description**: XML sitemap format for search engines
- **Use Case**: SEO, web crawling
- **Complexity**: Low - XML with URL entries

### 46. **Robots.txt**
- **Extensions**: `.robots.txt`
- **Type**: Text, rule-based
- **Description**: Robots exclusion protocol format
- **Use Case**: Web crawling rules
- **Complexity**: Low - Simple directive format

### 47. **WebPagetest Format**
- **Extensions**: `.wpt`, `.webpagetest`
- **Type**: Text (JSON), test-based
- **Description**: WebPagetest results format
- **Use Case**: Web performance testing
- **Complexity**: Medium - JSON with test results

## Additional JSON Variants

### 48. **JSON Lines (NDJSON) - Enhanced**
- **Extensions**: `.ndjson`, `.jsonl` (already supported, but could add streaming variants)
- **Type**: Text, line-based
- **Description**: Newline-delimited JSON with streaming support
- **Use Case**: Streaming data, log aggregation
- **Complexity**: Low - Already supported, but could add streaming variants

### 49. **JSON Patch**
- **Extensions**: `.jsonpatch`
- **Type**: Text (JSON), patch-based
- **Description**: JSON Patch format (RFC 6902)
- **Use Case**: JSON document updates, API patches
- **Example**: `[{"op": "add", "path": "/foo", "value": "bar"}]`
- **Complexity**: Low - JSON array of patch operations

### 50. **JSON Merge Patch**
- **Extensions**: `.jsonmerge`
- **Type**: Text (JSON), patch-based
- **Description**: JSON Merge Patch format (RFC 7396)
- **Use Case**: JSON document merging
- **Complexity**: Low - JSON object representing merge

### 51. **JSON-LD (JSON for Linking Data)**
- **Extensions**: `.jsonld`, `.json-ld`
- **Type**: Text (JSON), document-based
- **Description**: JSON-LD format for linked data
- **Use Case**: Semantic web, linked data
- **Complexity**: Medium - JSON with @context and @id

### 52. **JSON Schema**
- **Extensions**: `.schema.json`, `.jsonschema`
- **Type**: Text (JSON), schema-based
- **Description**: JSON Schema format
- **Use Case**: Data validation, API documentation
- **Complexity**: Medium - JSON with schema definitions

### 53. **JSON API Format**
- **Extensions**: `.jsonapi`
- **Type**: Text (JSON), document-based
- **Description**: JSON API specification format
- **Use Case**: REST API responses
- **Complexity**: Medium - JSON with specific structure

## Additional Time Series Formats

### 54. **InfluxDB Line Protocol**
- **Extensions**: `.influx`, `.line`
- **Type**: Text, line-based
- **Description**: InfluxDB line protocol format
- **Use Case**: Time series database imports
- **Example**: `cpu,host=server01,region=us-west value=0.64 1434055562000000000`
- **Complexity**: Low - Simple key-value format with tags

### 55. **TimescaleDB Format**
- **Extensions**: `.timescale`, `.tsdb`
- **Type**: Text (CSV or binary), row-based
- **Description**: TimescaleDB export format
- **Use Case**: Time series database exports
- **Complexity**: Medium - PostgreSQL-based format

### 56. **RRDtool Format**
- **Extensions**: `.rrd`
- **Type**: Binary, round-robin database
- **Description**: Round-Robin Database format
- **Use Case**: Time series data storage
- **Complexity**: High - Requires rrdtool library

### 57. **Whisper Format (Graphite)**
- **Extensions**: `.wsp`
- **Type**: Binary, time series
- **Description**: Graphite Whisper time series format
- **Use Case**: Time series metrics storage
- **Complexity**: High - Requires whisper library

### 58. **Carbon Format**
- **Extensions**: `.carbon`
- **Type**: Text, line-based
- **Description**: Graphite Carbon plaintext protocol
- **Use Case**: Metrics ingestion
- **Example**: `metric.path 123.45 1609459200`
- **Complexity**: Low - Simple metric format

### 59. **StatsD Format**
- **Extensions**: `.statsd`
- **Type**: Text, line-based
- **Description**: StatsD metrics format
- **Use Case**: Application metrics
- **Example**: `gorets:1|c\ngaugor:333|g\nglork:320|ms`
- **Complexity**: Low - Simple metric format with types

## Additional Big Data/Streaming Formats

### 60. **Apache Pulsar Format**
- **Extensions**: `.pulsar` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Apache Pulsar message format
- **Use Case**: Event streaming
- **Complexity**: High - Already supported, could add variants

### 61. **Apache Kafka Format**
- **Extensions**: `.kafka` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Apache Kafka message format
- **Use Case**: Event streaming
- **Complexity**: High - Already supported, could add variants

### 62. **RabbitMQ Format**
- **Extensions**: `.rabbitmq`, `.amqp`
- **Type**: Binary, message-based
- **Description**: RabbitMQ message format (AMQP)
- **Use Case**: Message queue exports
- **Complexity**: High - Requires pika or amqp library

### 63. **Apache NiFi FlowFile Format**
- **Extensions**: `.flowfile`, `.nifi`
- **Type**: Binary, record-based
- **Description**: Apache NiFi FlowFile format
- **Use Case**: Data flow processing
- **Complexity**: High - Requires NiFi libraries

### 64. **Apache Airflow Log Format**
- **Extensions**: `.airflow.log`
- **Type**: Text, line-based
- **Description**: Apache Airflow task logs
- **Use Case**: Workflow orchestration logs
- **Complexity**: Medium - Structured logging format

### 65. **Apache Beam Format**
- **Extensions**: `.beam` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Apache Beam data format
- **Use Case**: Batch and stream processing
- **Complexity**: High - Already supported

### 66. **Apache Flink Format**
- **Extensions**: `.flink` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Apache Flink checkpoint format
- **Use Case**: Stream processing
- **Complexity**: High - Already supported

### 67. **Apache Samza Format**
- **Extensions**: `.samza`
- **Type**: Binary, message-based
- **Description**: Apache Samza message format
- **Use Case**: Stream processing
- **Complexity**: High - Requires Samza libraries

## Additional Database Export Formats

### 68. **PostgreSQL COPY Format**
- **Extensions**: `.pgcopy`, `.copy` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: PostgreSQL COPY format variants
- **Use Case**: PostgreSQL data exports
- **Complexity**: Medium - Already supported, could add variants

### 69. **MySQL Dump Format**
- **Extensions**: `.sql`, `.mysqldump` (already supported, but could add INSERT-only variants)
- **Type**: Text, statement-based
- **Description**: MySQL dump format (INSERT statements)
- **Use Case**: MySQL data exports
- **Complexity**: Medium - Already supported, could add INSERT parsing

### 70. **SQLite Format**
- **Extensions**: `.db`, `.sqlite` (already supported, but could add export formats)
- **Type**: Binary, table-based
- **Description**: SQLite database format
- **Use Case**: Embedded database exports
- **Complexity**: Medium - Already supported

### 71. **Cassandra SSTable Format**
- **Extensions**: `.sstable`, `.cassandra`
- **Type**: Binary, row-based
- **Description**: Apache Cassandra SSTable format
- **Use Case**: Cassandra data exports
- **Complexity**: High - Requires cassandra-driver or sstable-tools

### 72. **CouchDB Export Format**
- **Extensions**: `.couchdb`, `.couch`
- **Type**: Text (JSON), document-based
- **Description**: CouchDB document export format
- **Use Case**: CouchDB data exports
- **Complexity**: Low - JSONL format

### 73. **DynamoDB Export Format**
- **Extensions**: `.dynamodb`, `.dynamo`
- **Type**: Text (JSON), item-based
- **Description**: AWS DynamoDB export format
- **Use Case**: DynamoDB data exports
- **Complexity**: Medium - JSON with DynamoDB-specific types

### 74. **Riak Export Format**
- **Extensions**: `.riak`
- **Type**: Binary/Text, key-value based
- **Description**: Riak database export format
- **Use Case**: Riak data exports
- **Complexity**: Medium - Key-value format

### 75. **Neo4j Export Format**
- **Extensions**: `.neo4j`, `.cypher`
- **Type**: Text, statement-based
- **Description**: Neo4j Cypher export format
- **Use Case**: Graph database exports
- **Complexity**: Medium - Cypher query format

### 76. **ArangoDB Export Format**
- **Extensions**: `.arangodb`, `.arango`
- **Type**: Text (JSON), document-based
- **Description**: ArangoDB export format
- **Use Case**: Multi-model database exports
- **Complexity**: Low - JSONL format

### 77. **InfluxDB Export Format**
- **Extensions**: `.influxdb`, `.influx`
- **Type**: Text, line-based
- **Description**: InfluxDB export format
- **Use Case**: Time series database exports
- **Complexity**: Low - Line protocol format

### 78. **ClickHouse Format**
- **Extensions**: `.clickhouse`, `.ch`
- **Type**: Text (TSV), row-based
- **Description**: ClickHouse export format
- **Use Case**: Columnar database exports
- **Complexity**: Low - TSV format

### 79. **DuckDB Format**
- **Extensions**: `.duckdb`, `.ddb`
- **Type**: Binary, table-based
- **Description**: DuckDB database format
- **Use Case**: Analytical database exports
- **Complexity**: High - Requires duckdb library

### 80. **BigQuery Export Format**
- **Extensions**: `.bigquery`, `.bq`
- **Type**: Text (CSV/JSON), row-based
- **Description**: Google BigQuery export format
- **Use Case**: BigQuery data exports
- **Complexity**: Low - CSV or JSONL format

### 81. **Snowflake Export Format**
- **Extensions**: `.snowflake`
- **Type**: Text (CSV/JSON), row-based
- **Description**: Snowflake export format
- **Use Case**: Snowflake data exports
- **Complexity**: Low - CSV or JSON format

### 82. **Redshift Export Format**
- **Extensions**: `.redshift`
- **Type**: Text (CSV), row-based
- **Description**: AWS Redshift export format
- **Use Case**: Redshift data exports
- **Complexity**: Low - CSV format

### 83. **Hive Format**
- **Extensions**: `.hive`
- **Type**: Text (delimited), row-based
- **Description**: Apache Hive table format
- **Use Case**: Data warehouse exports
- **Complexity**: Medium - Delimited text format

### 84. **Presto Format**
- **Extensions**: `.presto`
- **Type**: Text (CSV/JSON), row-based
- **Description**: Presto query result format
- **Use Case**: Query result exports
- **Complexity**: Low - CSV or JSON format

## Additional Scientific/Specialized Formats

### 85. **GFF (General Feature Format)**
- **Extensions**: `.gff`, `.gff3`
- **Type**: Text, feature-based
- **Description**: Genome annotation format
- **Use Case**: Bioinformatics, genomics
- **Example**: `chr1\t.\texon\t1000\t2000\t.\t+\t.\tgene_id "gene1"`
- **Complexity**: Low - Tab-delimited format

### 86. **GTF (Gene Transfer Format)**
- **Extensions**: `.gtf`
- **Type**: Text, feature-based
- **Description**: Gene annotation format
- **Use Case**: Bioinformatics, genomics
- **Complexity**: Low - Similar to GFF

### 87. **BED Format**
- **Extensions**: `.bed`
- **Type**: Text, region-based
- **Description**: Browser Extensible Data format
- **Use Case**: Genomics, genome browsers
- **Example**: `chr1\t1000\t2000\tfeature1\t0\t+`
- **Complexity**: Low - Tab-delimited format

### 88. **VCF (Variant Call Format)**
- **Extensions**: `.vcf` (already supported, but could add BCF binary variant)
- **Type**: Text, variant-based
- **Description**: Variant call format
- **Use Case**: Genomics, variant analysis
- **Complexity**: Medium - Already supported, could add BCF

### 89. **BCF (Binary VCF)**
- **Extensions**: `.bcf`
- **Type**: Binary, variant-based
- **Description**: Binary variant call format
- **Use Case**: Genomics, variant analysis
- **Complexity**: High - Requires htslib/pysam

### 90. **GFF3 Format**
- **Extensions**: `.gff3`
- **Type**: Text, feature-based
- **Description**: GFF version 3 format
- **Use Case**: Genome annotation
- **Complexity**: Low - Tab-delimited with attributes

### 91. **MAF (Multiple Alignment Format)**
- **Extensions**: `.maf`
- **Type**: Text, alignment-based
- **Description**: Multiple sequence alignment format
- **Use Case**: Comparative genomics
- **Complexity**: Medium - Block-based format

### 92. **PHYLIP Format**
- **Extensions**: `.phy`, `.phylip`
- **Type**: Text, sequence-based
- **Description**: Phylogenetic data format
- **Use Case**: Phylogenetics, evolutionary biology
- **Complexity**: Medium - Fixed-width sequence format

### 93. **NEXUS Format**
- **Extensions**: `.nex`, `.nexus`
- **Type**: Text, block-based
- **Description**: Phylogenetic data format
- **Use Case**: Phylogenetics
- **Complexity**: Medium - Block-structured format

### 94. **Newick Format**
- **Extensions**: `.newick`, `.nwk`, `.tree`
- **Type**: Text, tree-based
- **Description**: Phylogenetic tree format
- **Use Case**: Phylogenetics, tree visualization
- **Example**: `(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);`
- **Complexity**: Low - Simple tree notation

### 95. **PDB Format (Protein Data Bank)**
- **Extensions**: `.pdb`
- **Type**: Text, record-based
- **Description**: Protein structure format
- **Use Case**: Structural biology, protein analysis
- **Complexity**: Medium - Record-based format with specific record types

### 96. **MMCIF Format**
- **Extensions**: `.cif`, `.mmcif`
- **Type**: Text, data-based
- **Description**: Macromolecular Crystallographic Information File
- **Use Case**: Structural biology
- **Complexity**: Medium - Key-value format with loops

### 97. **SDF Format (Structure Data Format)**
- **Extensions**: `.sdf`
- **Type**: Text, molecule-based
- **Description**: Chemical structure format
- **Use Case**: Chemistry, drug discovery
- **Complexity**: Medium - Molecule records with delimiters

### 98. **MOL Format**
- **Extensions**: `.mol`
- **Type**: Text, molecule-based
- **Description**: Chemical structure format
- **Use Case**: Chemistry, molecular modeling
- **Complexity**: Medium - Fixed-format molecule representation

### 99. **SMILES Format**
- **Extensions**: `.smi`, `.smiles`
- **Type**: Text, line-based
- **Description**: Simplified Molecular Input Line Entry System
- **Use Case**: Chemistry, cheminformatics
- **Example**: `CCO\tethanol\nCC(=O)O\tacetic acid`
- **Complexity**: Low - Simple line-based format

### 100. **InChI Format**
- **Extensions**: `.inchi`
- **Type**: Text, line-based
- **Description**: International Chemical Identifier
- **Use Case**: Chemistry, chemical identification
- **Complexity**: Low - Simple identifier format

### 101. **CML (Chemical Markup Language)**
- **Extensions**: `.cml`
- **Type**: Text (XML), molecule-based
- **Description**: XML-based chemical format
- **Use Case**: Chemistry, molecular data exchange
- **Complexity**: Medium - XML format for chemistry

### 102. **HDF5 Format**
- **Extensions**: `.h5`, `.hdf5` (already supported, but could add variants)
- **Type**: Binary, array-based
- **Description**: Hierarchical Data Format version 5
- **Use Case**: Scientific data, large arrays
- **Complexity**: High - Already supported

### 103. **HDF4 Format**
- **Extensions**: `.h4`, `.hdf`, `.hdf4`
- **Type**: Binary, array-based
- **Description**: Hierarchical Data Format version 4
- **Use Case**: Legacy scientific data
- **Complexity**: High - Requires hdf4 library

### 104. **Zarr Format**
- **Extensions**: `.zarr`
- **Type**: Binary, array-based
- **Description**: Chunked, compressed N-dimensional arrays
- **Use Case**: Scientific computing, cloud storage
- **Complexity**: High - Requires zarr library

### 105. **TIFF Format (for scientific data)**
- **Extensions**: `.tif`, `.tiff`
- **Type**: Binary, image-based
- **Description**: Tagged Image File Format (can contain scientific metadata)
- **Use Case**: Scientific imaging, microscopy
- **Complexity**: High - Requires PIL/Pillow or tifffile

### 106. **DICOM Format**
- **Extensions**: `.dcm`, `.dicom`
- **Type**: Binary, image-based
- **Description**: Digital Imaging and Communications in Medicine
- **Use Case**: Medical imaging, radiology
- **Complexity**: High - Requires pydicom library

### 107. **NIfTI Format**
- **Extensions**: `.nii`, `.nii.gz`, `.hdr`
- **Type**: Binary, image-based
- **Description**: Neuroimaging Informatics Technology Initiative format
- **Use Case**: Neuroimaging, brain imaging
- **Complexity**: High - Requires nibabel library

### 108. **MINC Format**
- **Extensions**: `.mnc`
- **Type**: Binary, image-based
- **Description**: Medical Imaging NetCDF format
- **Use Case**: Medical imaging
- **Complexity**: High - Requires pyminc library

### 109. **MGH/MGZ Format**
- **Extensions**: `.mgh`, `.mgz`
- **Type**: Binary, image-based
- **Description**: MGH/MGZ image format (FreeSurfer)
- **Use Case**: Neuroimaging
- **Complexity**: High - Requires nibabel or custom parser

### 110. **VTK Format**
- **Extensions**: `.vtk`
- **Type**: Text/Binary, mesh-based
- **Description**: Visualization Toolkit format
- **Use Case**: Scientific visualization, mesh data
- **Complexity**: Medium - Structured format for meshes

### 111. **PLY Format**
- **Extensions**: `.ply`
- **Type**: Text/Binary, mesh-based
- **Description**: Polygon File Format
- **Use Case**: 3D models, point clouds
- **Complexity**: Medium - Header + vertex/face data

### 112. **OBJ Format**
- **Extensions**: `.obj`
- **Type**: Text, mesh-based
- **Description**: Wavefront OBJ format
- **Use Case**: 3D models, computer graphics
- **Complexity**: Low - Simple line-based format

### 113. **STL Format**
- **Extensions**: `.stl`
- **Type**: Text/Binary, mesh-based
- **Description**: Stereolithography format
- **Use Case**: 3D printing, CAD
- **Complexity**: Medium - Triangle mesh format

### 114. **LAS/LAZ Format**
- **Extensions**: `.las`, `.laz`
- **Type**: Binary, point-based
- **Description**: LiDAR point cloud format
- **Use Case**: Remote sensing, surveying
- **Complexity**: High - Requires laspy library

### 115. **E57 Format**
- **Extensions**: `.e57`
- **Type**: Binary, point-based
- **Description**: ASTM E57 3D imaging data format
- **Use Case**: 3D scanning, point clouds
- **Complexity**: High - Requires pye57 library

### 116. **PCD Format (Point Cloud Data)**
- **Extensions**: `.pcd`
- **Type**: Text/Binary, point-based
- **Description**: PCL point cloud format
- **Use Case**: Point cloud processing
- **Complexity**: Medium - Header + point data

### 117. **XYZ Format**
- **Extensions**: `.xyz`
- **Type**: Text, point-based
- **Description**: Simple point cloud format
- **Use Case**: Point cloud data
- **Example**: `3\ncomment\nC 0.0 0.0 0.0\nH 1.0 0.0 0.0\nO 0.0 1.0 0.0`
- **Complexity**: Low - Simple coordinate format

## Additional Configuration/Data Formats

### 118. **XML Variants**
- **Extensions**: Various (already supported, but could add specific variants)
- **Type**: Text (XML), element-based
- **Description**: XML format (already supported, but could add specific schemas)
- **Use Case**: Various
- **Complexity**: Medium - Already supported

### 119. **RSS Format**
- **Extensions**: `.rss`, `.xml` (when RSS)
- **Type**: Text (XML), item-based
- **Description**: Really Simple Syndication format
- **Use Case**: Web feeds, news aggregation
- **Complexity**: Low - XML with item elements

### 120. **Atom Format**
- **Extensions**: `.atom`, `.xml` (when Atom)
- **Type**: Text (XML), entry-based
- **Description**: Atom Syndication Format
- **Use Case**: Web feeds, blog syndication
- **Complexity**: Low - XML with entry elements

### 121. **OPML Format**
- **Extensions**: `.opml`
- **Type**: Text (XML), outline-based
- **Description**: Outline Processor Markup Language
- **Use Case**: Feed lists, outlines
- **Complexity**: Low - XML outline format

### 122. **FOAF Format**
- **Extensions**: `.foaf`, `.rdf` (when FOAF)
- **Type**: Text (RDF/XML), person-based
- **Description**: Friend of a Friend format
- **Use Case**: Social networks, personal profiles
- **Complexity**: Medium - RDF format

### 123. **GPX Format**
- **Extensions**: `.gpx`
- **Type**: Text (XML), waypoint-based
- **Description**: GPS Exchange Format
- **Use Case**: GPS data, navigation
- **Complexity**: Low - XML with waypoint/track elements

### 124. **KML Format**
- **Extensions**: `.kml`
- **Type**: Text (XML), placemark-based
- **Description**: Keyhole Markup Language
- **Use Case**: Geographic data, Google Earth
- **Complexity**: Medium - XML with geographic features

### 125. **Shapefile Format**
- **Extensions**: `.shp`, `.shx`, `.dbf`
- **Type**: Binary, feature-based
- **Description**: ESRI Shapefile format
- **Use Case**: GIS, geographic data
- **Complexity**: High - Requires pyshp or geopandas

### 126. **GeoPackage Format**
- **Extensions**: `.gpkg`
- **Type**: Binary, feature-based
- **Description**: OGC GeoPackage format
- **Use Case**: GIS, mobile mapping
- **Complexity**: High - SQLite-based format

### 127. **GML Format**
- **Extensions**: `.gml`
- **Type**: Text (XML), feature-based
- **Description**: Geography Markup Language
- **Use Case**: GIS, geographic data exchange
- **Complexity**: Medium - XML format for geography

### 128. **TopoJSON Format**
- **Extensions**: `.topojson`
- **Type**: Text (JSON), geometry-based
- **Description**: Topology-preserving GeoJSON variant
- **Use Case**: Web mapping, geographic visualization
- **Complexity**: Medium - JSON with topology

### 129. **MBTiles Format**
- **Extensions**: `.mbtiles`
- **Type**: Binary, tile-based
- **Description**: Mapbox Tiles format (SQLite-based)
- **Use Case**: Web mapping, tile storage
- **Complexity**: High - SQLite with tile metadata

### 130. **CSVW (CSV on the Web)**
- **Extensions**: `.csvw`, `.csv-metadata.json`
- **Type**: Text (JSON + CSV), metadata-based
- **Description**: CSV with metadata annotations
- **Use Case**: Linked data, semantic web
- **Complexity**: Medium - CSV with JSON-LD metadata

## Additional Serialization Formats

### 131. **BSON Format**
- **Extensions**: `.bson` (already supported, but could add variants)
- **Type**: Binary, document-based
- **Description**: Binary JSON format
- **Use Case**: MongoDB, binary JSON
- **Complexity**: Medium - Already supported

### 132. **MessagePack Format**
- **Extensions**: `.msgpack` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: Binary serialization format
- **Use Case**: Efficient data serialization
- **Complexity**: Medium - Already supported

### 133. **CBOR Format**
- **Extensions**: `.cbor` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: Concise Binary Object Representation
- **Use Case**: IoT, efficient serialization
- **Complexity**: Medium - Already supported

### 134. **UBJSON Format**
- **Extensions**: `.ubj`, `.ubjson` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: Universal Binary JSON
- **Use Case**: Efficient JSON serialization
- **Complexity**: Medium - Already supported

### 135. **SMILE Format**
- **Extensions**: `.smile` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: Binary JSON format
- **Use Case**: Efficient JSON serialization
- **Complexity**: Medium - Already supported

### 136. **Ion Format**
- **Extensions**: `.ion` (already supported, but could add variants)
- **Type**: Binary/Text, value-based
- **Description**: Amazon Ion format
- **Use Case**: Data exchange, document databases
- **Complexity**: Medium - Already supported

### 137. **Bencode Format**
- **Extensions**: `.torrent`, `.bencode` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: BitTorrent encoding format
- **Use Case**: BitTorrent, peer-to-peer
- **Complexity**: Low - Already supported

### 138. **ASN.1 Format**
- **Extensions**: `.asn1`, `.der` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: Abstract Syntax Notation One
- **Use Case**: Telecommunications, cryptography
- **Complexity**: High - Already supported

### 139. **Protobuf Format**
- **Extensions**: `.protobuf`, `.pb` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Protocol Buffers
- **Use Case**: Efficient data serialization
- **Complexity**: High - Already supported

### 140. **Cap'n Proto Format**
- **Extensions**: `.capnp` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Cap'n Proto serialization
- **Use Case**: High-performance serialization
- **Complexity**: High - Already supported

### 141. **Thrift Format**
- **Extensions**: `.thrift` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Apache Thrift
- **Use Case**: Cross-language RPC
- **Complexity**: High - Already supported

### 142. **FlatBuffers Format**
- **Extensions**: `.fbs` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: FlatBuffers serialization
- **Use Case**: Game development, mobile apps
- **Complexity**: High - Already supported

### 143. **FlexBuffers Format**
- **Extensions**: `.flexbuf` (already supported, but could add variants)
- **Type**: Binary, value-based
- **Description**: FlexBuffers (schema-less FlatBuffers)
- **Use Case**: Flexible binary serialization
- **Complexity**: High - Already supported

### 144. **Avro Format**
- **Extensions**: `.avro` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Apache Avro
- **Use Case**: Big data, schema evolution
- **Complexity**: High - Already supported

### 145. **ORC Format**
- **Extensions**: `.orc` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: Optimized Row Columnar format
- **Use Case**: Big data, columnar storage
- **Complexity**: High - Already supported

### 146. **Parquet Format**
- **Extensions**: `.parquet` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: Apache Parquet
- **Use Case**: Big data, columnar storage
- **Complexity**: High - Already supported

### 147. **Arrow Format**
- **Extensions**: `.arrow`, `.feather` (already supported, but could add variants)
- **Type**: Binary, column-based
- **Description**: Apache Arrow
- **Use Case**: In-memory columnar data
- **Complexity**: High - Already supported

## Additional Specialized Formats

### 148. **iCal Format**
- **Extensions**: `.ics`, `.ical` (already supported, but could add variants)
- **Type**: Text, event-based
- **Description**: iCalendar format
- **Use Case**: Calendar data, scheduling
- **Complexity**: Medium - Already supported

### 149. **VCF Format (vCard)**
- **Extensions**: `.vcf`, `.vcard` (already supported, but could add variants)
- **Type**: Text, contact-based
- **Description**: vCard format
- **Use Case**: Contact information
- **Complexity**: Medium - Already supported

### 150. **LDIF Format**
- **Extensions**: `.ldif` (already supported, but could add variants)
- **Type**: Text, entry-based
- **Description**: LDAP Data Interchange Format
- **Use Case**: LDAP directory exports
- **Complexity**: Medium - Already supported

### 151. **MBOX Format**
- **Extensions**: `.mbox` (already supported, but could add variants)
- **Type**: Text, message-based
- **Description**: Mailbox format
- **Use Case**: Email archives
- **Complexity**: Medium - Already supported

### 152. **EML Format**
- **Extensions**: `.eml` (already supported, but could add variants)
- **Type**: Text, message-based
- **Description**: Email message format
- **Use Case**: Individual email messages
- **Complexity**: Medium - Already supported

### 153. **MHTML Format**
- **Extensions**: `.mhtml`, `.mht` (already supported, but could add variants)
- **Type**: Text, message-based
- **Description**: MIME HTML format
- **Use Case**: Web page archives
- **Complexity**: Medium - Already supported

### 154. **WARC Format**
- **Extensions**: `.warc`, `.arc` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Web ARChive format
- **Use Case**: Web archiving
- **Complexity**: Medium - Already supported

### 155. **CDX Format**
- **Extensions**: `.cdx` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: CDX index format
- **Use Case**: Web archive indexing
- **Complexity**: Low - Already supported

### 156. **Apache Log Format**
- **Extensions**: `.log`, `.access.log` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: Apache web server log format
- **Use Case**: Web server logs
- **Complexity**: Medium - Already supported

### 157. **GELF Format**
- **Extensions**: `.gelf` (already supported, but could add variants)
- **Type**: Text (JSON), line-based
- **Description**: Graylog Extended Log Format
- **Use Case**: Centralized logging
- **Complexity**: Low - Already supported

### 158. **CEF Format**
- **Extensions**: `.cef` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: Common Event Format
- **Use Case**: Security event logging
- **Complexity**: Medium - Already supported

### 159. **ILP Format**
- **Extensions**: `.ilp` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: InfluxDB Line Protocol
- **Use Case**: Time series data ingestion
- **Complexity**: Low - Already supported

### 160. **Annotated CSV Format**
- **Extensions**: `.annotatedcsv` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: CSV with annotations
- **Use Case**: InfluxDB, time series data
- **Complexity**: Medium - Already supported

### 161. **LTSV Format**
- **Extensions**: `.ltsv` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: Labeled Tab-Separated Values
- **Use Case**: Structured logging
- **Complexity**: Low - Already supported

### 162. **PSV Format**
- **Extensions**: `.psv` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: Pipe-Separated Values
- **Use Case**: Data exchange
- **Complexity**: Low - Already supported

### 163. **SSV Format**
- **Extensions**: `.ssv` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: Space-Separated Values
- **Use Case**: Data exchange
- **Complexity**: Low - Already supported

### 164. **FWF Format**
- **Extensions**: `.fwf`, `.fixed` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: Fixed-Width Format
- **Use Case**: Legacy data formats
- **Complexity**: Medium - Already supported

### 165. **CSV Format**
- **Extensions**: `.csv`, `.tsv` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: Comma-Separated Values
- **Use Case**: Tabular data exchange
- **Complexity**: Low - Already supported

### 166. **JSON Format**
- **Extensions**: `.json` (already supported, but could add streaming variants)
- **Type**: Text, document-based
- **Description**: JavaScript Object Notation
- **Use Case**: Data exchange, APIs
- **Complexity**: Low - Already supported

### 167. **JSONL Format**
- **Extensions**: `.jsonl`, `.ndjson` (already supported, but could add variants)
- **Type**: Text, line-based
- **Description**: JSON Lines format
- **Use Case**: Streaming data, logs
- **Complexity**: Low - Already supported

### 168. **YAML Format**
- **Extensions**: `.yaml`, `.yml` (already supported, but could add variants)
- **Type**: Text, document-based
- **Description**: YAML Ain't Markup Language
- **Use Case**: Configuration files, data serialization
- **Complexity**: Medium - Already supported

### 169. **TOML Format**
- **Extensions**: `.toml` (already supported, but could add variants)
- **Type**: Text, document-based
- **Description**: Tom's Obvious Minimal Language
- **Use Case**: Configuration files
- **Complexity**: Low - Already supported

### 170. **INI Format**
- **Extensions**: `.ini`, `.conf` (already supported, but could add variants)
- **Type**: Text, section-based
- **Description**: INI configuration format
- **Use Case**: Configuration files
- **Complexity**: Low - Already supported

### 171. **HOCON Format**
- **Extensions**: `.hocon`, `.conf` (when HOCON) (already supported, but could add variants)
- **Type**: Text, document-based
- **Description**: Human-Optimized Config Object Notation
- **Use Case**: Configuration files (Play, Akka)
- **Complexity**: Medium - Already supported

### 172. **EDN Format**
- **Extensions**: `.edn` (already supported, but could add variants)
- **Type**: Text, value-based
- **Description**: Extensible Data Notation
- **Use Case**: Clojure data exchange
- **Complexity**: Medium - Already supported

### 173. **XML Format**
- **Extensions**: `.xml` (already supported, but could add streaming variants)
- **Type**: Text, element-based
- **Description**: Extensible Markup Language
- **Use Case**: Data exchange, documents
- **Complexity**: Medium - Already supported

### 174. **RDF/XML Format**
- **Extensions**: `.rdf`, `.rdf.xml` (already supported, but could add variants)
- **Type**: Text (XML), triple-based
- **Description**: Resource Description Framework XML
- **Use Case**: Semantic web, linked data
- **Complexity**: High - Already supported

### 175. **Turtle Format**
- **Extensions**: `.ttl`, `.turtle` (already supported, but could add variants)
- **Type**: Text, triple-based
- **Description**: Turtle RDF format
- **Use Case**: Semantic web, RDF data
- **Complexity**: Medium - Already supported

### 176. **N-Triples Format**
- **Extensions**: `.nt`, `.ntriples` (already supported, but could add variants)
- **Type**: Text, triple-based
- **Description**: N-Triples RDF format
- **Use Case**: Semantic web, RDF data
- **Complexity**: Low - Already supported

### 177. **N-Quads Format**
- **Extensions**: `.nq`, `.nquads` (already supported, but could add variants)
- **Type**: Text, quad-based
- **Description**: N-Quads RDF format
- **Use Case**: Semantic web, RDF with contexts
- **Complexity**: Low - Already supported

### 178. **Excel Formats**
- **Extensions**: `.xls`, `.xlsx` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: Microsoft Excel formats
- **Use Case**: Spreadsheet data
- **Complexity**: High - Already supported

### 179. **ODS Format**
- **Extensions**: `.ods` (already supported, but could add variants)
- **Type**: Binary (ZIP/XML), row-based
- **Description**: OpenDocument Spreadsheet
- **Use Case**: Spreadsheet data
- **Complexity**: High - Already supported

### 180. **DBF Format**
- **Extensions**: `.dbf` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: dBASE database format
- **Use Case**: Legacy database files
- **Complexity**: Medium - Already supported

### 181. **SAS Format**
- **Extensions**: `.sas7bdat`, `.sas` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: SAS dataset format
- **Use Case**: Statistical analysis
- **Complexity**: High - Already supported

### 182. **Stata Format**
- **Extensions**: `.dta`, `.stata` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: Stata dataset format
- **Use Case**: Statistical analysis
- **Complexity**: High - Already supported

### 183. **SPSS Format**
- **Extensions**: `.sav`, `.spss` (already supported, but could add variants)
- **Type**: Binary, row-based
- **Description**: SPSS dataset format
- **Use Case**: Statistical analysis
- **Complexity**: High - Already supported

### 184. **PX Format**
- **Extensions**: `.px` (already supported, but could add variants)
- **Type**: Text, table-based
- **Description**: PC-Axis format
- **Use Case**: Statistical data exchange
- **Complexity**: Medium - Already supported

### 185. **GeoJSON Format**
- **Extensions**: `.geojson` (already supported, but could add variants)
- **Type**: Text (JSON), feature-based
- **Description**: Geographic JSON format
- **Use Case**: Geographic data, web mapping
- **Complexity**: Medium - Already supported

### 186. **HDF5 Format**
- **Extensions**: `.h5`, `.hdf5` (already supported, but could add variants)
- **Type**: Binary, array-based
- **Description**: Hierarchical Data Format version 5
- **Use Case**: Scientific data, large arrays
- **Complexity**: High - Already supported

### 187. **Delta Lake Format**
- **Extensions**: `.delta` (already supported, but could add variants)
- **Type**: Binary, table-based
- **Description**: Delta Lake format
- **Use Case**: Data lake storage, ACID transactions
- **Complexity**: High - Already supported

### 188. **Iceberg Format**
- **Extensions**: `.iceberg` (already supported, but could add variants)
- **Type**: Binary, table-based
- **Description**: Apache Iceberg format
- **Use Case**: Data lake storage, table format
- **Complexity**: High - Already supported

### 189. **Hudi Format**
- **Extensions**: `.hudi` (already supported, but could add variants)
- **Type**: Binary, table-based
- **Description**: Apache Hudi format
- **Use Case**: Data lake storage, incremental processing
- **Complexity**: High - Already supported

### 190. **TFRecord Format**
- **Extensions**: `.tfrecord`, `.tfrecords` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: TensorFlow record format
- **Use Case**: Machine learning data
- **Complexity**: High - Already supported

### 191. **SequenceFile Format**
- **Extensions**: `.seq`, `.sequencefile` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Hadoop SequenceFile format
- **Use Case**: Hadoop data storage
- **Complexity**: High - Already supported

### 192. **RecordIO Format**
- **Extensions**: `.recordio` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: RecordIO format
- **Use Case**: Machine learning, data pipelines
- **Complexity**: Medium - Already supported

### 193. **Kafka Format**
- **Extensions**: `.kafka` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Apache Kafka message format
- **Use Case**: Event streaming
- **Complexity**: High - Already supported

### 194. **Pulsar Format**
- **Extensions**: `.pulsar` (already supported, but could add variants)
- **Type**: Binary, message-based
- **Description**: Apache Pulsar message format
- **Use Case**: Event streaming
- **Complexity**: High - Already supported

### 195. **Flink Format**
- **Extensions**: `.flink` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Apache Flink checkpoint format
- **Use Case**: Stream processing
- **Complexity**: High - Already supported

### 196. **Beam Format**
- **Extensions**: `.beam` (already supported, but could add variants)
- **Type**: Binary, record-based
- **Description**: Apache Beam data format
- **Use Case**: Batch and stream processing
- **Complexity**: High - Already supported

### 197. **SQLite Format**
- **Extensions**: `.db`, `.sqlite` (already supported, but could add export formats)
- **Type**: Binary, table-based
- **Description**: SQLite database format
- **Use Case**: Embedded databases
- **Complexity**: Medium - Already supported

### 198. **MySQL Dump Format**
- **Extensions**: `.sql`, `.mysqldump` (already supported, but could add INSERT-only variants)
- **Type**: Text, statement-based
- **Description**: MySQL dump format
- **Use Case**: MySQL data exports
- **Complexity**: Medium - Already supported

### 199. **PostgreSQL COPY Format**
- **Extensions**: `.pgcopy`, `.copy` (already supported, but could add variants)
- **Type**: Text, row-based
- **Description**: PostgreSQL COPY format
- **Use Case**: PostgreSQL data exports
- **Complexity**: Medium - Already supported

### 200. **Pickle Format**
- **Extensions**: `.pkl`, `.pickle` (already supported, but could add variants)
- **Type**: Binary, object-based
- **Description**: Python pickle format
- **Use Case**: Python object serialization
- **Complexity**: Medium - Already supported

## Summary Statistics

- **Total Formats Listed**: 200+
- **Already Implemented**: ~70 formats
- **New Suggestions**: ~130 formats
- **Low Complexity**: ~40 formats
- **Medium Complexity**: ~50 formats
- **High Complexity**: ~40 formats

## New Formats Not Yet Implemented (Top Recommendations)

The following formats are **NOT** currently implemented and represent the best opportunities for expansion:

### High Priority (Easy to Implement, High Value)

1. **Logfmt** (#2) - Modern structured logging, widely used
2. **LTSV** (#1) - Already in suggestions, simple implementation
3. **JSON5** (#9) - Human-readable JSON with comments
4. **HJSON** (#10) - Human-readable JSON variant
5. **JSONC** (#11) - JSON with C-style comments
6. **Prometheus Format** (#12) - Metrics export format
7. **Graphite Format** (#13) - Time series metrics
8. **InfluxDB Line Protocol** (#54) - Time series ingestion
9. **StatsD Format** (#59) - Application metrics
10. **HAR** (#7) - HTTP Archive format for web debugging
11. **Syslog** (#3) - Standard system logging (RFC 3164/5424)
12. **Nginx Access Log** (#4) - Web server logs
13. **IIS Log Format** (#5) - Windows web server logs
14. **Log4j Format** (#6) - Java application logs
15. **Env/Dotenv Format** (#28, #29) - Environment configuration
16. **Properties Format** (#27) - Java properties files
17. **MongoDB Export Format** (#18) - Database exports (JSONL/CSV)
18. **SQL Server BCP Format** (#20) - SQL Server exports
19. **Oracle SQL*Loader Format** (#21) - Oracle exports
20. **FASTA/FASTQ Format** (#23) - Biological sequences

### Medium Priority (Moderate Complexity, Good Value)

21. **PCAP Format** (#8) - Network packet capture
22. **OpenTSDB Format** (#14) - Time series database
23. **Windows Event Log (EVTX)** (#34) - Windows system logs
24. **Journald Format** (#35) - systemd journal
25. **Logstash Format** (#36) - Log processing
26. **Fluentd Format** (#37) - Log forwarding
27. **Graylog Format** (#38) - Centralized logging
28. **Splunk Format** (#39) - Log analysis
29. **ELK Stack Format** (#40) - Elasticsearch exports
30. **WebVTT** (#43) - Video subtitles
31. **SRT Format** (#44) - Subtitle format
32. **Sitemap XML** (#45) - SEO sitemaps
33. **RSS Format** (#119) - Web feeds
34. **Atom Format** (#120) - Web feeds
35. **GPX Format** (#123) - GPS data
36. **KML Format** (#124) - Geographic data
37. **JSON-LD** (#51) - Linked data
38. **JSON Patch** (#49) - JSON updates
39. **JSON Schema** (#52) - Data validation
40. **TimescaleDB Format** (#55) - Time series exports

### Specialized Domains (Higher Complexity, Domain-Specific)

41. **NetCDF Format** (#25) - Scientific data
42. **FITS Format** (#26) - Astronomy data
43. **PLINK Format** (#22) - Genetics data
44. **SAM/BAM Format** (#24) - Sequence alignment
45. **GFF/GTF Format** (#85, #86) - Genome annotation
46. **BED Format** (#87) - Genomic regions
47. **BCF Format** (#89) - Binary VCF
48. **FASTA/FASTQ** (#23) - Biological sequences
49. **PDB Format** (#95) - Protein structures
50. **SDF/MOL Format** (#97, #98) - Chemical structures
51. **SMILES Format** (#99) - Chemical notation
52. **DICOM Format** (#106) - Medical imaging
53. **NIfTI Format** (#107) - Neuroimaging
54. **LAS/LAZ Format** (#114) - LiDAR point clouds
55. **PCD Format** (#116) - Point cloud data
56. **VTK Format** (#110) - Scientific visualization
57. **PLY/OBJ/STL** (#111, #112, #113) - 3D models
58. **Shapefile Format** (#125) - GIS data
59. **GeoPackage Format** (#126) - Mobile mapping
60. **Cassandra SSTable** (#71) - NoSQL exports
61. **CouchDB Export** (#72) - Document database
62. **DynamoDB Export** (#73) - AWS database
63. **Neo4j Export** (#75) - Graph database
64. **ClickHouse Format** (#78) - Columnar database
65. **BigQuery Export** (#80) - Google analytics
66. **Snowflake Export** (#81) - Data warehouse
67. **Redshift Export** (#82) - AWS data warehouse
68. **Hive Format** (#83) - Data warehouse
69. **Redis RDB Format** (#19) - Key-value store
70. **RabbitMQ Format** (#62) - Message queue

## Priority Recommendations

Based on common use cases and ease of implementation, here are the **top 10 recommended formats** to add:

1. **LTSV** - Simple, commonly used in web services
2. **Logfmt** - Modern structured logging, widely adopted
3. **HAR** - Web development and debugging
4. **JSON5** - Configuration files, human-readable JSON
5. **Prometheus Format** - Monitoring and metrics
6. **Graphite Format** - Time series data
7. **Syslog** - System logging standard
8. **Nginx Access Log** - Web server logs
9. **MongoDB Export Format** - Database exports
10. **Env/Dotenv Format** - Application configuration

## Implementation Notes

- **Low Complexity**: Can be implemented similar to existing text formats (CSV, JSONL)
- **Medium Complexity**: Requires parsing logic but follows established patterns
- **High Complexity**: Requires external libraries or specialized format knowledge

Most formats follow similar patterns to existing implementations:
- Line-based formats → Similar to JSONL, Apache Log
- Key-value formats → Similar to INI, Properties
- Binary formats → Similar to BSON, MessagePack
- Structured text → Similar to XML, JSON

## Format Detection

When adding new formats, consider:
1. File extension mapping in `detect.py`
2. Content-based detection (magic bytes, header patterns)
3. Integration with existing codec support (compression)
4. Documentation in `docs/formats/` directory
5. Test fixtures in `tests/fixtures/` directory
