#!/usr/bin/env python3
"""
Script to find missing fixture combinations for data types and codecs.
"""

# Text-based data types that can be compressed
TEXT_DATATYPES = ['csv', 'json', 'jsonl', 'ndjson', 'xml']

# Compression codecs and their extensions
CODECS = {
    'br': 'Brotli',
    'bz2': 'BZip2', 
    'gz': 'GZip',
    'lz4': 'LZ4',
    'xz': 'LZMA',
    'zip': 'ZIP',
    'zst': 'ZStandard',
    'zstd': 'ZStandard'  # alternative extension
}

# Existing fixtures in tests/fixtures/
import os

fixtures_dir = 'tests/fixtures'
existing_files = set()
if os.path.exists(fixtures_dir):
    existing_files = {f for f in os.listdir(fixtures_dir) if os.path.isfile(os.path.join(fixtures_dir, f))}

print("=" * 80)
print("MISSING FIXTURE COMBINATIONS ANALYSIS")
print("=" * 80)
print()

# Expected combinations: datatype.codec
expected_combinations = set()
for datatype in TEXT_DATATYPES:
    for codec_ext in CODECS.keys():
        if codec_ext == 'zstd':  # Skip zstd, use zst instead
            continue
        expected_combinations.add(f"2cols6rows.{datatype}.{codec_ext}")
        # Also check for alternative naming patterns
        if datatype == 'json':
            expected_combinations.add(f"2cols6rows_array.{datatype}.{codec_ext}")
            expected_combinations.add(f"2cols6rows_tag.{datatype}.{codec_ext}")
        if datatype == 'jsonl':
            expected_combinations.add(f"2cols6rows_flat.{datatype}.{codec_ext}")
            expected_combinations.add(f"2cols6rows_flat.ndjson.{codec_ext}")  # ndjson as extension
        if datatype == 'xml':
            expected_combinations.add(f"books.{datatype}.{codec_ext}")

# Find missing combinations
missing_combinations = expected_combinations - existing_files

# Group by datatype
missing_by_datatype = {}
for combo in missing_combinations:
    parts = combo.split('.')
    if len(parts) >= 2:
        datatype = parts[-2]  # Second to last is datatype
        codec = parts[-1]     # Last is codec
        if datatype not in missing_by_datatype:
            missing_by_datatype[datatype] = []
        missing_by_datatype[datatype].append((combo, codec))

# Also check what we have
existing_by_datatype = {}
for f in existing_files:
    parts = f.split('.')
    if len(parts) >= 2:
        datatype = parts[-2]
        codec = parts[-1]
        if codec in CODECS:
            if datatype not in existing_by_datatype:
                existing_by_datatype[datatype] = []
            existing_by_datatype[datatype].append((f, codec))

print("EXISTING COMBINATIONS:")
print("-" * 80)
for datatype in sorted(TEXT_DATATYPES):
    if datatype in existing_by_datatype:
        print(f"\n{datatype.upper()}:")
        for f, _codec in sorted(existing_by_datatype[datatype]):
            print(f"  ✓ {f}")

print("\n" + "=" * 80)
print("MISSING COMBINATIONS:")
print("-" * 80)

total_missing = 0
for datatype in sorted(TEXT_DATATYPES):
    if datatype in missing_by_datatype:
        print(f"\n{datatype.upper()} - Missing {len(missing_by_datatype[datatype])} combinations:")
        # Group by codec
        by_codec = {}
        for combo, codec in missing_by_datatype[datatype]:
            if codec not in by_codec:
                by_codec[codec] = []
            by_codec[codec].append(combo)
        
        for codec in sorted(by_codec.keys()):
            print(f"  • {CODECS.get(codec, codec)} (.{codec}):")
            for combo in sorted(by_codec[codec]):
                print(f"    - {combo}")
                total_missing += 1

print("\n" + "=" * 80)
print(f"SUMMARY: {total_missing} missing fixture files")
print("=" * 80)

# Generate a summary table
print("\nCOVERAGE MATRIX:")
print("-" * 80)
print(f"{'Data Type':<12} ", end="")
for codec_ext in sorted([c for c in CODECS.keys() if c != 'zstd']):
    print(f"{CODECS[codec_ext][:6]:<8}", end="")
print()

for datatype in sorted(TEXT_DATATYPES):
    print(f"{datatype:<12} ", end="")
    for codec_ext in sorted([c for c in CODECS.keys() if c != 'zstd']):
        # Check if combination exists
        found = False
        for f in existing_files:
            if f".{datatype}.{codec_ext}" in f:
                found = True
                break
        print(f"{'✓' if found else '✗':<8}", end="")
    print()



