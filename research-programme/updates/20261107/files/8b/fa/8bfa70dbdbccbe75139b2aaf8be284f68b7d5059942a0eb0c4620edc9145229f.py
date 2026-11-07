from __future__ import annotations

import mpmath as mp
import numpy as np
from scipy.interpolate import CubicSpline


JOINS = ((1e-4, 2e-4), (5e-5, 1e-4))


def checked_grid(values):
    grid = np.asarray(values, dtype=float)
    if grid.ndim != 1 or grid.size < 2 or not np.all(np.isfinite(grid)):
        raise ValueError("A finite one-dimensional grid with at least two nodes is required")
    if np.any(grid <= 0) or np.any(np.diff(grid) <= 0):
        raise ValueError("Frequency nodes must be positive and strictly increasing")
    return grid.copy()


class NodalFeatures:
    def __init__(self, original, tail_frequency):
        epoch = original.epochs[0]
        self.basis = original.basis
        self.frequency = checked_grid(epoch.frequency)
        self.tail_frequency = checked_grid(tail_frequency)
        basis_values = np.asarray(epoch.basis.evaluate(self.frequency), dtype=float)
        if basis_values.ndim != 2 or basis_values.shape[0] != self.frequency.size:
            raise ValueError("Basis values must have one row per master frequency")
        if not np.all(np.isfinite(basis_values)):
            raise ValueError("Nonfinite basis values")
        self.profile_count = basis_values.shape[1]
        self.spectral_count = self.profile_count + self.tail_frequency.size
        self.coefficient_count = self.spectral_count + 1
        identity = np.eye(self.tail_frequency.size)
        log_master, log_tail = np.log(self.frequency), np.log(self.tail_frequency)
        interpolation = np.column_stack([
            np.interp(log_master, log_tail, column) for column in identity.T
        ])
        self.splines = []
        for lower, upper in JOINS:
            phase = np.clip((self.frequency - lower) / (upper - lower), 0, 1)
            blend = phase**3 * (10 - 15 * phase + 6 * phase**2)
            data = np.column_stack((
                basis_values * blend[:, None],
                (1 - blend[:, None]) * self.frequency[:, None] * interpolation,
            ))
            self.splines.append(CubicSpline(log_master, data, axis=0, extrapolate=False))

    def evaluate(self, frequency, join, derivative=False):
        if join not in (0, 1):
            raise ValueError("Join must be 0 or 1")
        values = np.asarray(frequency, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("Nonfinite evaluation frequency")
        if np.any(values < self.frequency[0] * (1 - 1e-10)) or np.any(values > self.frequency[-1] * (1 + 1e-10)):
            raise ValueError("Evaluation outside the retained master-frequency domain")
        coordinate = np.log(np.clip(values, self.frequency[0], self.frequency[-1]))
        result = self.splines[join](coordinate, nu=1 if derivative else 0)
        return result / values[..., None] if derivative else result


def make_bundle(retained_bundle_class, features, coefficients, inputs):
    columns = [list(column) for column in coefficients]
    if not columns or len(columns) % 2:
        raise ValueError("State columns must be supplied in pairs for the two retained joins")
    if any(len(column) != features.coefficient_count for column in columns):
        raise ValueError("Expected profile coefficients, every tail slope node, then gas")

    class NodalBundle(retained_bundle_class):
        def __init__(self):
            self.features, self.basis, self.inputs = features, features.basis, inputs
            self.high = np.empty((features.coefficient_count, len(columns)))
            self.low = np.empty_like(self.high)
            with mp.workdps(80):
                for column_index, values in enumerate(columns):
                    for row_index, value in enumerate(values):
                        exact = mp.mpf(value)
                        upper = float(exact)
                        lower = float(exact - mp.mpf(upper))
                        if not np.isfinite(upper) or not np.isfinite(lower):
                            raise ValueError("Nonfinite history coefficient")
                        self.high[row_index, column_index] = upper
                        self.low[row_index, column_index] = lower
            self.gas = self.high[-1, ::2].tolist()

    return NodalBundle()


def coefficient_difference(before, after):
    if len(before) != len(after):
        raise ValueError("History coefficient lengths differ")
    with mp.workdps(80):
        difference = [mp.mpf(second) - mp.mpf(first) for first, second in zip(before, after)]
        if not all(mp.isfinite(value) for value in difference):
            raise ValueError("Nonfinite history difference")
        return difference
