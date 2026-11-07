from __future__ import annotations

import math

import mpmath as mp
import numpy as np
from scipy.linalg import solve_banded

from adjoint_readout import AdjointNodalFeatures


class CorrelatedNodalFeatures(AdjointNodalFeatures):
    def difference_weights(self, frequency, shifts):
        frequency = float(frequency)
        shifts = np.asarray(shifts, dtype=float).reshape(-1)
        if not math.isfinite(frequency) or not self.frequency[0] <= frequency <= self.frequency[-1]:
            raise ValueError("Reference frequency outside the retained master grid")
        if shifts.size > self.chunk_size:
            raise ValueError("Difference weights require a bounded query chunk")
        if not np.isfinite(shifts).all() or np.any(shifts <= -frequency):
            raise ValueError("Finite shifts to positive frequencies required")
        increments = np.log1p(shifts / frequency)
        slopes = np.zeros((self.frequency.size, shifts.size))
        direct = np.zeros_like(slopes)
        with mp.workdps(80):
            origin = mp.mpf(math.log(frequency))
            for query, increment in enumerate(increments):
                destination = origin + mp.mpf(float(increment))
                if not mp.mpf(float(self.coordinate[0])) <= destination <= mp.mpf(float(self.coordinate[-1])):
                    raise ValueError("Shifted frequency outside the retained master grid")
                if increment == 0:
                    continue
                direction = 1 if increment > 0 else -1
                cursor, endpoint = sorted((origin, destination))
                position = min(max(int(np.searchsorted(self.coordinate, float(cursor), side="right") - 1), 0), self.frequency.size - 2)
                while position > 0 and mp.mpf(float(self.coordinate[position])) > cursor:
                    position -= 1
                while position < self.frequency.size - 2 and mp.mpf(float(self.coordinate[position + 1])) <= cursor:
                    position += 1
                while cursor < endpoint:
                    knot = mp.mpf(float(self.coordinate[position]))
                    stop = min(endpoint, mp.mpf(float(self.coordinate[position + 1])))
                    width = float(self.widths[position])
                    phase = float((cursor - knot) / mp.mpf(width))
                    change = float((stop - cursor) / mp.mpf(width))
                    first = direction * change * (6 * phase**2 - 6 * phase + change * (6 * phase - 3) + 2 * change**2)
                    slope_first = direction * width * change * (3 * phase**2 - 4 * phase + 1 + change * (3 * phase - 2) + change**2)
                    slope_last = direction * width * change * (3 * phase**2 - 2 * phase + change * (3 * phase - 1) + change**2)
                    direct[position, query] += first
                    direct[position + 1, query] -= first
                    slopes[position, query] += slope_first
                    slopes[position + 1, query] += slope_last
                    cursor = stop
                    position += 1
        adjoint = solve_banded((1, 1), self.transpose_band, slopes, check_finite=False)
        return direct + self.rhs_map.T @ adjoint

    def difference(self, frequency, shifts, join):
        if join not in (0, 1):
            raise ValueError("Join must be 0 or 1")
        values = np.asarray(shifts, dtype=float)
        flattened = values.reshape(-1)
        output = np.empty((flattened.size, self.spectral_count))
        blend = self.blends[join]
        for start in range(0, flattened.size, self.chunk_size):
            stop = min(start + self.chunk_size, flattened.size)
            weights = self.difference_weights(frequency, flattened[start:stop])
            output[start:stop, :self.profile_count] = (weights * blend[:, None]).T @ self.basis_values
            output[start:stop, self.profile_count:] = (self.tail_map.T @ (weights * ((1 - blend) * self.frequency)[:, None])).T
        return output.reshape(values.shape + (self.spectral_count,))
