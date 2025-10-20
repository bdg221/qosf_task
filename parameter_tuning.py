"""This file will include the functions for parameter tuning."""

from scipy.optimize import differential_evolution
import numpy as np
import time

from cost import frobenius_norm, trace_norm, count_comparison


def optimize_angles_and_time() -> list[tuple[list[float], float]]:
    """This function runs the global optimizer to find the optimized
    paramters for the U3 gates.

    Returns:
        A list of tuples that include the optimized angles and the time
        it took to perform the optimization."""
    bounds = [
        (0, np.pi),
        (0, 2 * np.pi),
        (0, 2 * np.pi),
        (0, np.pi),
        (0, 2 * np.pi),
        (0, 2 * np.pi),
    ]
    start_time = time.time()
    trace_result = differential_evolution(trace_norm, bounds)
    trace_optimized_angles = trace_result.x
    trace_time = time.time() - start_time

    start_time = time.time()
    frobenius_result = differential_evolution(frobenius_norm, bounds)
    frobenius_optimized_angles = frobenius_result.x
    frobenius_time = time.time() - start_time

    start_time = time.time()
    count_result = differential_evolution(count_comparison, bounds)
    count_optimized_angles = count_result.x
    count_time = time.time() - start_time

    return [
        (trace_optimized_angles, trace_time),
        (frobenius_optimized_angles, frobenius_time),
        (count_optimized_angles, count_time),
    ]
