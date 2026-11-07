import numpy as np
from scipy.interpolate import CubicSpline


def difference_using_retained_splines(features, frequency, shifts, join, difference_function, block_size=8):
    if join not in (0, 1):
        raise ValueError("Join must be 0 or 1")
    if not isinstance(block_size, int) or not 1 <= block_size <= 8:
        raise ValueError("Retained column blocks must contain one to eight fields")
    frequency = float(frequency)
    values = np.asarray(shifts, dtype=float)
    flattened = values.reshape(-1)
    if not np.isfinite(frequency) or not features.frequency[0] <= frequency <= features.frequency[-1]:
        raise ValueError("Reference frequency outside the retained master grid")
    if not np.isfinite(flattened).all() or np.any(flattened <= -frequency):
        raise ValueError("Finite shifts to positive frequencies required")
    destinations = np.log(frequency) + np.log1p(flattened / frequency)
    if np.any(destinations < features.coordinate[0]) or np.any(destinations > features.coordinate[-1]):
        raise ValueError("Shifted frequency outside the retained master grid")
    output = np.empty((flattened.size, features.spectral_count))
    blend = features.blends[join]
    for start in range(0, features.profile_count, block_size):
        stop = min(start + block_size, features.profile_count)
        data = features.basis_values[:, start:stop] * blend[:, None]
        spline = CubicSpline(features.coordinate, data, axis=0, extrapolate=False)
        output[:, start:stop] = difference_function(spline, frequency, flattened)
    for start in range(0, features.tail_frequency.size, block_size):
        stop = min(start + block_size, features.tail_frequency.size)
        interpolation = features.tail_map[:, start:stop].toarray()
        data = (1 - blend[:, None]) * features.frequency[:, None] * interpolation
        spline = CubicSpline(features.coordinate, data, axis=0, extrapolate=False)
        output[:, features.profile_count + start:features.profile_count + stop] = difference_function(spline, frequency, flattened)
    return output.reshape(values.shape + (features.spectral_count,))
