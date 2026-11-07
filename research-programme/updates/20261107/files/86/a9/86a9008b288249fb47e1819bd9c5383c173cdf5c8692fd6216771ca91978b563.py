from soft_matching_common import *


def cold_events(order):
    cosines, weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2 * math.pi * (np.arange(2 * order) + .5) / (2 * order)
    cosine = np.repeat(cosines, len(azimuth))
    azimuth = np.tile(azimuth, order)
    direction = np.column_stack([np.sqrt(1 - cosine ** 2) * np.cos(azimuth), np.sqrt(1 - cosine ** 2) * np.sin(azimuth), cosine])
    frames = thermal_wave.prior.prior.frames(direction)
    initial_frame = thermal_wave.prior.prior.frames(np.array([0., 0., 1.]))
    return dict(incident=np.ones_like(cosine), outgoing=np.ones_like(cosine), cosine=cosine,
        weight=np.repeat(weights / (2 * len(azimuth) / order), 2 * order),
        final_direction=direction, final_frame=frames, jones=frames.swapaxes(-1, -2) @ initial_frame)


def weighted_angular(degree, order):
    events = cold_events(order)
    first, second, names = thermal_wave.prior.angular_correlations(events, degree)
    weights = events['weight'] * (1 - events['cosine'])
    gain = .375 * np.einsum('n,abn->ab', weights, first + first.swapaxes(0, 1))
    loss = .75 * np.sum(weights * (1 + events['cosine'] ** 2)) / (2 * degree + 1)
    return gain - loss * np.eye(len(names)), names, float(np.sum(events['weight']))
