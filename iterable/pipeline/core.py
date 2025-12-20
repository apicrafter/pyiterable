# -*- coding: utf-8 -*-
from ..base import BaseIterable
from typing import Callable
import time
import logging

logger = logging.getLogger(__name__)


def pipeline(source: BaseIterable, destination: BaseIterable, process_func: Callable[[dict, dict], dict], trigger_func:Callable[[dict, dict], None] = None, trigger_on:int=1000, final_func: Callable[[dict, dict], None] = None, reset_iterables: bool = True, skip_nulls: bool = True, start_state:dict={}, debug:bool = False):
    """Wrapper over Pipeline class to simplify data processing pipelines execution"""
    runner = Pipeline(source=source, destination=destination, process_func=process_func, trigger_func=trigger_func, trigger_on=trigger_on, final_func=final_func, reset_iterables=reset_iterables, skip_nulls=skip_nulls, start_state=start_state)
    runner.run(debug)


class Pipeline:
    """Data processing pipeline that read data and process it"""
    def __init__(self, source: BaseIterable, destination: BaseIterable = None, process_func: Callable[[dict, dict], dict]=None, trigger_func:Callable[[dict, dict], None] = None, trigger_on:int=1000, final_func: Callable[[dict, dict], None] = None, reset_iterables: bool = True, skip_nulls: bool = True, start_state:dict={}):
        self.source = source
        self.destination = destination
        self.process_func = process_func
        self.trigger_func = trigger_func
        self.trigger_on = trigger_on
        self.final_func = final_func
        self.reset_iterables = reset_iterables
        self.skip_nulls = skip_nulls
        self.start_state = start_state


    def run(self, debug:bool = False):
        """Execute pipeline"""
        stats = {'rec_count' : 0, 'nulls' : 0, 'exceptions' : 0, 'time_start' : time.time()}    
        state = self.start_state
        if self.reset_iterables:
            self.source.reset()
            if self.destination is not None:
                self.destination.reset()
        
        for record in self.source:
            try:
                result = self.process_func(record, state)
                if result is None:
                    if not self.skip_nulls:
                        stats['nulls'] += 1
                        if self.destination is not None:
                            self.destination.write(result)                
                else:
                    if self.destination is not None:
                        self.destination.write(result)                
            except Exception as e:
                logger.error(
                    f"Error processing record #{stats['rec_count'] + 1}: {e}",
                    exc_info=debug
                )
                stats['exceptions'] += 1
                if debug:
                    raise
            stats['rec_count'] += 1
            if stats['rec_count'] % self.trigger_on == 0 and self.trigger_func is not None:
                try:
                    self.trigger_func(stats, state)
                except Exception as e:
                    logger.error(
                        f"Error in trigger function at record #{stats['rec_count']}: {e}",
                        exc_info=debug
                    )
                    if debug:
                        raise
        stats['time_end'] = time.time()
        stats['duration'] = stats['time_end'] - stats['time_start']
        if self.final_func is not None:
            self.final_func(stats, state)
        return stats