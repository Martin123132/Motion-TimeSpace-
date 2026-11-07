from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.linalg import solve_banded

from nodal_readout import JOINS, checked_grid


class AdjointNodalFeatures:
    def __init__(self, original, tail_frequency, chunk_size=8):
        epoch = original.epochs[0]
        self.basis = original.basis
        self.frequency = checked_grid(epoch.frequency)
        self.tail_frequency = checked_grid(tail_frequency)
        if self.frequency.size < 4:
            raise ValueError("The adjoint not-a-knot implementation requires at least four master nodes")
        if not isinstance(chunk_size, int) or chunk_size < 1 or chunk_size > 32:
            raise ValueError("Query chunks must contain between one and 32 frequencies")
        self.chunk_size = chunk_size
        self.coordinate = np.log(self.frequency)
        self.widths = np.diff(self.coordinate)
        self.basis_values = np.asarray(epoch.basis.evaluate(self.frequency), dtype=float)
        if self.basis_values.ndim != 2 or self.basis_values.shape[0] != self.frequency.size or not np.isfinite(self.basis_values).all():
            raise ValueError("Invalid master-grid basis values")
        self.profile_count = self.basis_values.shape[1]
        self.spectral_count = self.profile_count + self.tail_frequency.size
        self.coefficient_count = self.spectral_count + 1
        self.blends = []
        for lower, upper in JOINS:
            phase = np.clip((self.frequency - lower) / (upper - lower), 0, 1)
            self.blends.append(phase**3 * (10 - 15 * phase + 6 * phase**2))
        count = self.frequency.size
        band = np.zeros((3, count))
        band[1, 1:-1] = 2 * (self.widths[:-1] + self.widths[1:])
        band[0, 2:] = self.widths[:-1]
        band[2, :-2] = self.widths[1:]
        first_span, last_span = self.coordinate[2] - self.coordinate[0], self.coordinate[-1] - self.coordinate[-3]
        band[1, 0], band[0, 1] = self.widths[1], first_span
        band[1, -1], band[2, -2] = self.widths[-2], last_span
        self.transpose_band = np.zeros_like(band)
        self.transpose_band[1] = band[1]
        self.transpose_band[0, 1:] = band[2, :-1]
        self.transpose_band[2, :-1] = band[0, 1:]
        interior = np.arange(1, count - 1)
        before = 3 * self.widths[1:] / self.widths[:-1]
        after = 3 * self.widths[:-1] / self.widths[1:]
        first_before = (self.widths[0] + 2 * first_span) * self.widths[1] / (first_span * self.widths[0])
        first_after = self.widths[0]**2 / (first_span * self.widths[1])
        last_before = self.widths[-1]**2 / (last_span * self.widths[-2])
        last_after = (2 * last_span + self.widths[-1]) * self.widths[-2] / (last_span * self.widths[-1])
        rows = np.r_[interior, interior, interior, [0, 0, 0, count - 1, count - 1, count - 1]]
        columns = np.r_[interior - 1, interior, interior + 1, [0, 1, 2, count - 3, count - 2, count - 1]]
        values = np.r_[-before, before - after, after,
            [-first_before, first_before - first_after, first_after, -last_before, last_before - last_after, last_after]]
        self.rhs_map = sparse.csr_matrix((values, (rows, columns)), shape=(count, count))
        log_tail = np.log(self.tail_frequency)
        positions = np.clip(np.searchsorted(log_tail, self.coordinate, side="right") - 1, 0, log_tail.size - 2)
        fractions = np.clip((self.coordinate - log_tail[positions]) / (log_tail[positions + 1] - log_tail[positions]), 0, 1)
        self.tail_map = sparse.csr_matrix((np.r_[1 - fractions, fractions],
            (np.tile(np.arange(count), 2), np.r_[positions, positions + 1])), shape=(count, self.tail_frequency.size))

    def weights(self, frequency, derivative=False):
        values = np.asarray(frequency, dtype=float).reshape(-1)
        if not np.isfinite(values).all() or np.any(values < self.frequency[0] * (1 - 1e-10)) or np.any(values > self.frequency[-1] * (1 + 1e-10)):
            raise ValueError("Evaluation outside the finite retained master-frequency domain")
        coordinate = np.log(np.clip(values, self.frequency[0], self.frequency[-1]))
        positions = np.clip(np.searchsorted(self.coordinate, coordinate, side="right") - 1, 0, self.frequency.size - 2)
        width = self.widths[positions]
        phase = (coordinate - self.coordinate[positions]) / width
        if derivative:
            direct_first = (6 * phase**2 - 6 * phase) / width
            direct_last = -direct_first
            slope_first = 3 * phase**2 - 4 * phase + 1
            slope_last = 3 * phase**2 - 2 * phase
        else:
            direct_first = 2 * phase**3 - 3 * phase**2 + 1
            direct_last = -2 * phase**3 + 3 * phase**2
            slope_first = width * (phase**3 - 2 * phase**2 + phase)
            slope_last = width * (phase**3 - phase**2)
        queries = np.arange(values.size)
        slopes = np.zeros((self.frequency.size, values.size))
        slopes[positions, queries] = slope_first
        slopes[positions + 1, queries] = slope_last
        adjoint = solve_banded((1, 1), self.transpose_band, slopes, check_finite=False)
        result = self.rhs_map.T @ adjoint
        result[positions, queries] += direct_first
        result[positions + 1, queries] += direct_last
        return result / values[None, :] if derivative else result

    def evaluate(self, frequency, join, derivative=False):
        if join not in (0, 1):
            raise ValueError("Join must be 0 or 1")
        values = np.asarray(frequency, dtype=float)
        flattened = values.reshape(-1)
        output = np.empty((flattened.size, self.spectral_count))
        blend = self.blends[join]
        for start in range(0, flattened.size, self.chunk_size):
            stop = min(start + self.chunk_size, flattened.size)
            weights = self.weights(flattened[start:stop], derivative)
            output[start:stop, :self.profile_count] = (weights * blend[:, None]).T @ self.basis_values
            output[start:stop, self.profile_count:] = (self.tail_map.T @ (weights * ((1 - blend) * self.frequency)[:, None])).T
        return output.reshape(values.shape + (self.spectral_count,))

    def storage_bytes(self):
        arrays = [self.frequency, self.tail_frequency, self.coordinate, self.widths,
            self.basis_values, self.transpose_band, *self.blends]
        return sum(value.nbytes for value in arrays) + sum(value.nbytes for matrix in (self.rhs_map, self.tail_map)
            for value in (matrix.data, matrix.indices, matrix.indptr))
