# author: bloodspork
# date  : 20220427

from audioop import avg
import time
import functools
import logging

_func_timing_dict = {}

def get_func_timing_dict():
    global _func_timing_dict
    return _func_timing_dict

def _collect(funcName, duration):
    global _func_timing_dict
    if funcName not in _func_timing_dict:
        _func_timing_dict[funcName] = []
    _func_timing_dict[funcName].append(duration)

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ret = func(*args, **kwargs)
        end_time = time.perf_counter()
        _collect(f"{func.__name__!r}", end_time - start_time)
        return ret
    return wrapper

def log_duration_summary(loggingLevel = logging.DEBUG):
    ftd = get_func_timing_dict()
    msg = "Durations Summary\n"
    for funcName, duration_list in ftd.items():
        tot_time = sum(duration_list)
        num_calls = len(duration_list)
        avg_time = tot_time / num_calls
        msg += funcName.rjust(30, ' ')
        msg += f"  #calls: {str(num_calls).rjust(10)}" \
               f"  avg: {str(round(avg_time, 3)).rjust(10, ' ')}" \
               f"  tot: {str(round(tot_time, 3)).rjust(10, ' ')}\n"             
    logging.log(loggingLevel, msg)


