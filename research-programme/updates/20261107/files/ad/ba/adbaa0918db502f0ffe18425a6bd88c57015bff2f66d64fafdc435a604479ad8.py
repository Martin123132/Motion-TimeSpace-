from frequency_grid_common import *
from resolved_redistribution import incoming_rule


def electron_nodes(theta, radial=3, folded=True):
    electrons = {}
    for identity in population_nodes(theta, 4, 5, radial=radial, polar=3, azimuthal=8):
        electrons[tuple(identity['velocity'])] = identity['electron_weight']
    for electron_index, (velocity, measure) in enumerate(electrons.items()):
        azimuth = electron_index % 8
        if folded and azimuth > 4:
            continue
        multiplicity = 2 if folded and azimuth in [1, 2, 3] else 1
        yield dict(velocity=list(velocity), electron_weight=measure, electron_index=electron_index,
            azimuth_index=azimuth, reflection_multiplicity=multiplicity)


def physical_nodes(theta, seed_order=3, radial=3, folded=True):
    cosines, hard_weights = np.polynomial.legendre.leggauss(5)
    incoming = list(incoming_rule(seed_order, 1e-5, 24.))
    index = 0
    for electron in electron_nodes(theta, radial, folded):
        for frequency, seed_weight in incoming:
            for cosine, hard_weight in zip(cosines, hard_weights):
                yield dict(index=index, frequency=float(frequency), seed_weight=float(seed_weight),
                    cosine=float(cosine), hard_weight=float(hard_weight), **electron)
                index += 1


def parameters_and_weight(theta, identity):
    parameters = weak.source.context(theta * identity['frequency'], identity['cosine'], np.array(identity['velocity']), theta)
    weight = identity['electron_weight'] * identity['reflection_multiplicity'] * identity['seed_weight']
    weight *= identity['frequency']**2 / math.expm1(identity['frequency']) / I3
    weight *= 2 * np.pi * identity['hard_weight'] * parameters['born_differential_over_thomson']
    return parameters, weight


def replace_incoming(previous, replacements):
    assert set(replacements) == {'difference', 'virtual', 'state'}
    updated = dict(previous)
    mixed = {}
    for component, value in replacements.items():
        key = 'incoming-' + component
        assert key in previous and value.shape == previous[key].shape
        mixed[component] = value - previous[key]
        updated[key] = value
    assert set(updated) == set(previous)
    return updated, mixed
