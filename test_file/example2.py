import time

def log_execution_time(func):
    """
    A decorator that logs the execution time of the function it decorates.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper

# Example function using the decorator
@log_execution_time
def slow_addition(a, b):
    """
    A function that performs addition with a delay to simulate a slow operation.
    """
    time.sleep(0.5)  # Simulate a slow operation
    return a + b

@log_execution_time
def fast_multiplication(a, b):
    """
    A function that performs multiplication quickly.
    """
    return a * b
