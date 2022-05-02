# author: bloodspork
# date  : 20220427

import time
import functools
import logging

_func_timing_dict = {}


def get_func_timing_dict():
    global _func_timing_dict
    return _func_timing_dict


def collect(funcName, duration):
    if duration < 0:
        return

    global _func_timing_dict
    if funcName not in _func_timing_dict:
        _func_timing_dict[funcName] = []
    _func_timing_dict[funcName].append(duration)


class RegionTimer():
    def __init__(self, name):
        global _func_timing_dict
        self.func_timing_dict = _func_timing_dict
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()

    def __exit__(self, type, value, traceback):
        self.end_time = time.perf_counter()
        collect(self.name, self.end_time - self.start_time)


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        ret = func(*args, **kwargs)
        end_time = time.perf_counter()
        collect(f"{func.__name__!r}", end_time - start_time)
        return ret
    return wrapper


def log_duration_summary(overallDuration, loggingLevel=logging.DEBUG):
    ftd = get_func_timing_dict()
    msg = ""
    accounted_tot = 0
    for funcName, duration_list in sorted(ftd.items()):
        tot_time = sum(duration_list)
        num_calls = len(duration_list)
        avg_time = tot_time / num_calls
        pct = round(tot_time / overallDuration * 100)
        msg += funcName.rjust(30, ' ')
        msg += f"  #calls: {str(num_calls).rjust(10)}" \
               f"  avg: {str(round(avg_time, 3)).rjust(10, ' ')}" \
               f"  tot: {str(round(tot_time, 3)).rjust(10, ' ')}" \
               f"  pct: {str(pct).rjust(10, ' ')}%\n"
        accounted_tot += tot_time

    if msg != "":
        msg = "Durations Summary\n" + msg
        msg += f"Accounts for {round(accounted_tot / overallDuration * 100)}" \
               f"% of total duration ({round(overallDuration, 3)})"
        logging.log(loggingLevel, msg)
