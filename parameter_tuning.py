"""This file will include the functions for parameter tuning."""

import time

import numpy as np
from scipy.optimize import differential_evolution, minimize

from cost import count_comparison, frobenius_norm, trace_norm, trace_overlap_cost

bounds = [(0, 2 * np.pi)] * 6


def optimize_angles_and_time_all() -> list[tuple[list[float], float], str]:
    """This function runs the global optimizer to find the optimized
    paramters for the U3 gates.

    Returns:
        A list of tuples that include the optimized angles and the time
        it took to perform the optimization."""

    overlap_optimized_angles, overlap_time = optimize_with_trace_overlap()

    trace_optimized_angles, trace_time = optimize_with_trace_norm()

    frobenius_optimized_angles, frobenius_time = optimize_with_frobenius()

    count_optimized_angles, count_time = optimize_with_counts()

    return [
        (overlap_optimized_angles, overlap_time, "trace_overlap_cost"),
        (trace_optimized_angles, trace_time, "trace_norm"),
        (frobenius_optimized_angles, frobenius_time, "frobenius_norm"),
        (count_optimized_angles, count_time, "count_comparison"),
    ]


def optimize_with_trace_overlap() -> tuple[list[float], float]:
    """This function runs the global optimizer with the trace norm cost
    function.

    Returns:
        A tuple of the optimized angles and the time it took to perform the
        optimization."""
    start_time = time.time()
    trace_result = minimize(
        trace_overlap_cost,
        x0=[0, 0, 0, 0, 0, 0],
        bounds=bounds,
        method="Powell",  # "SLSQP",  # or 'L-BFGS-B', 'TNC', 'Powell'
        tol=1e-8,
    )
    # trace_result = differential_evolution(trace_norm, bounds)
    trace_optimized_angles = trace_result.x
    trace_time = time.time() - start_time
    return (trace_optimized_angles, trace_time)


def optimize_with_trace_norm() -> tuple[list[float], float]:
    """This function runs the global optimizer with the trace norm cost
    function.

    Returns:
        A tuple of the optimized angles and the time it took to perform the
        optimization."""
    start_time = time.time()
    trace_result = minimize(
        trace_norm,
        x0=[0, 0, 0, 0, 0, 0],
        bounds=bounds,
        method="Powell",  # "SLSQP",  # or 'L-BFGS-B', 'TNC', 'Powell'
        tol=1e-8,
    )
    # trace_result = differential_evolution(trace_norm, bounds)
    trace_optimized_angles = trace_result.x
    trace_time = time.time() - start_time
    return (trace_optimized_angles, trace_time)


def optimize_with_frobenius() -> tuple[list[float], float]:
    """This function runs the global optimizer with the frobenius norm cost
    function.

    Returns:
        A tuple of the optimized angles and the time it took to perform the
        optimization."""
    start_time = time.time()
    frobenius_result = minimize(
        frobenius_norm,
        x0=[0, 0, 0, 0, 0, 0],
        bounds=bounds,
        method="Powell",  # "SLSQP",  # or 'L-BFGS-B', 'TNC', 'Powell'
        tol=1e-8,
    )
    # frobenius_result = differential_evolution(frobenius_norm, bounds)
    frobenius_optimized_angles = frobenius_result.x
    frobenius_time = time.time() - start_time
    return (frobenius_optimized_angles, frobenius_time)


def optimize_with_counts() -> tuple[list[float], float]:
    """This function runs the global optimizer with the counts comparison cost
    function.

    Returns:
        A tuple of the optimized angles and the time it took to perform the
        optimization."""
    start_time = time.time()
    count_result = differential_evolution(
        count_comparison, bounds, maxiter=10, popsize=10
    )
    count_optimized_angles = count_result.x
    count_time = time.time() - start_time
    return (count_optimized_angles, count_time)
