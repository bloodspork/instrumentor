import time
import logging

from instrument import timeit, log_duration_summary

@timeit
def test_func_sleep_1():
    time.sleep(1)

@timeit
def test_func_sleep_3():
    time.sleep(3)

def setup_logging():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

if __name__ == "__main__":
    setup_logging()

    start_time = time.perf_counter()

    test_func_sleep_3()
    for i in range(7):
        test_func_sleep_1()

    end_time = time.perf_counter()
    log_duration_summary(end_time - start_time)
