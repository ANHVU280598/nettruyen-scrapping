import time
import json
import traceback
import logging
import sys





logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(message)s')

def retry_on_exception(retries=5, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error at {func.__name__}, attempt {attempt + 1}/{retries}: {e}")
                    time.sleep(delay)
            raise
        return wrapper
    return decorator
