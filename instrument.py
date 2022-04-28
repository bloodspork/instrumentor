# author: bloodspork
# date  : 20220427

import time
import functools
import logging

_func_timing_dict = {}

def _collect(funcName, duration):
    global func_timing_dict
    if funcName not in func_timing_dict:
        func_timing_dict[funcName] = duration
    else:
        _func_timing_dict[funcName] += duration


def timeit(func):
    @functools.wraps(func)
    def generic_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ret = func(*args, **kwargs)
        end_time = time.perf_counter()
        _collect(f"{func.__name__!r}", end_time - start_time)
        return ret


def getDurationsSummary():
    return _func_timing_dict


def logDurationsSummary(loggingLevel = logging.DEBUG):
    ftd = getDurationsSummary()
    ret = "Durations Summary\n"
    for k,v in ftd:
        ret += f"{k}: {v}\n"
    logging.log(loggingLevel, ret)


