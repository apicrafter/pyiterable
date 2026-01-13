import logging
import time
from collections.abc import Callable

from ..base import BaseIterable

logger = logging.getLogger(__name__)


def pipeline(
    source: BaseIterable,
    destination: BaseIterable,
    process_func: Callable[[dict, dict], dict],
    trigger_func: Callable[[dict, dict], None] = None,
    trigger_on: int = 1000,
    final_func: Callable[[dict, dict], None] = None,
    reset_iterables: bool = True,
    skip_nulls: bool = True,
    start_state: dict = None,
    debug: bool = False,
    batch_size: int = 1000,
):
    """Wrapper over Pipeline class to simplify data processing pipelines execution"""
    if start_state is None:
        start_state = {}
    runner = Pipeline(
        source=source,
        destination=destination,
        process_func=process_func,
        trigger_func=trigger_func,
        trigger_on=trigger_on,
        final_func=final_func,
        reset_iterables=reset_iterables,
        skip_nulls=skip_nulls,
        start_state=start_state,
        batch_size=batch_size,
    )
    runner.run(debug)


class Pipeline:
    """Data processing pipeline that read data and process it"""

    def __init__(
        self,
        source: BaseIterable,
        destination: BaseIterable = None,
        process_func: Callable[[dict, dict], dict] = None,
        trigger_func: Callable[[dict, dict], None] = None,
        trigger_on: int = 1000,
        final_func: Callable[[dict, dict], None] = None,
        reset_iterables: bool = True,
        skip_nulls: bool = True,
        start_state: dict = None,
        batch_size: int = 1000,
    ):
        if start_state is None:
            start_state = {}
        self.source = source
        self.destination = destination
        self.process_func = process_func
        self.trigger_func = trigger_func
        self.trigger_on = trigger_on
        self.final_func = final_func
        self.reset_iterables = reset_iterables
        self.skip_nulls = skip_nulls
        self.start_state = start_state
        self.batch_size = batch_size

    def run(self, debug: bool = False):
        """Execute pipeline"""
        stats = {"rec_count": 0, "nulls": 0, "exceptions": 0, "time_start": time.time()}
        state = self.start_state
        if self.reset_iterables:
            self.source.reset()
            if self.destination is not None:
                self.destination.reset()

        batch: list[dict] = []
        can_bulk_write = (
            self.destination is not None
            and hasattr(self.destination, "write_bulk")
            and self.batch_size
            and self.batch_size > 1
        )

        def flush_batch():
            nonlocal batch
            if self.destination is None or not batch:
                batch = []
                return
            if can_bulk_write:
                try:
                    self.destination.write_bulk(batch)
                except Exception:
                    # Fallback to per-record writes if destination's bulk path errors.
                    for item in batch:
                        self.destination.write(item)
            else:
                for item in batch:
                    self.destination.write(item)
            batch = []

        for record in self.source:
            try:
                result = self.process_func(record, state)
                if result is None:
                    if not self.skip_nulls:
                        stats["nulls"] += 1
                        if self.destination is not None:
                            # Preserve existing behavior (even though many destinations expect dicts).
                            flush_batch()
                            self.destination.write(result)
                else:
                    if self.destination is not None:
                        if can_bulk_write:
                            batch.append(result)
                            if len(batch) >= self.batch_size:
                                flush_batch()
                        else:
                            self.destination.write(result)
            except Exception as e:
                logger.error(f"Error processing record #{stats['rec_count'] + 1}: {e}", exc_info=debug)
                stats["exceptions"] += 1
                if debug:
                    raise
            stats["rec_count"] += 1
            if stats["rec_count"] % self.trigger_on == 0 and self.trigger_func is not None:
                try:
                    flush_batch()
                    self.trigger_func(stats, state)
                except Exception as e:
                    logger.error(f"Error in trigger function at record #{stats['rec_count']}: {e}", exc_info=debug)
                    if debug:
                        raise
        flush_batch()
        stats["time_end"] = time.time()
        stats["duration"] = stats["time_end"] - stats["time_start"]
        if self.final_func is not None:
            self.final_func(stats, state)
        return stats
