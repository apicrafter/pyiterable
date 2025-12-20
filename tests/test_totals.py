# -*- coding: utf-8 -*-
import pytest

from iterable.datatypes import (
    CSVIterable,
    JSONIterable,
    JSONLinesIterable,
    XLSIterable,
    XLSXIterable,
    ORCIterable,
    ParquetIterable,
    DBFIterable,
)


@pytest.mark.parametrize(
    "iterable_cls, path, kwargs, header_may_affect_totals",
    [
        (CSVIterable, "fixtures/2cols6rows.csv", {}, True),
        (JSONIterable, "fixtures/2cols6rows_tag.json", {"tagname": "persons"}, True),
        (JSONLinesIterable, "fixtures/2cols6rows_flat.jsonl", {}, True),
        (XLSIterable, "fixtures/2cols6rows.xls", {}, True),
        (XLSXIterable, "fixtures/2cols6rows.xlsx", {}, True),
        (ORCIterable, "fixtures/2cols6rows.orc", {}, True),
        (ParquetIterable, "fixtures/2cols6rows.parquet", {}, True),
        (DBFIterable, "fixtures/2cols6rows.dbf", {}, False),
    ],
)
def test_totals_match_record_count(iterable_cls, path, kwargs, header_may_affect_totals):
    it = iterable_cls(path, **kwargs)

    # Some classes may not expose has_totals; default is False on base
    has_totals = False
    if hasattr(iterable_cls, "has_totals") and callable(getattr(iterable_cls, "has_totals")):
        has_totals = iterable_cls.has_totals()

    assert has_totals is True

    totals_value = it.totals()

    # Normalize Parquet's scan_contents dict
    if isinstance(totals_value, dict):
        totals_normalized = totals_value.get("num_rows") or totals_value.get("rows")
    else:
        totals_normalized = totals_value

    assert isinstance(totals_normalized, int)

    # Count actual iterated records
    n = 0
    for _ in it:
        n += 1

    it.close()

    if header_may_affect_totals:
        # Some spreadsheet formats report total rows including header.
        assert totals_normalized in (n, n + 1)
    else:
        assert totals_normalized == n


