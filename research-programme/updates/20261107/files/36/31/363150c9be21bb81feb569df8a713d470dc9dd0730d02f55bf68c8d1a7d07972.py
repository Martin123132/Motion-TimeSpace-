from radial_common import *
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


def physical_nodes(theta, part, radial=3, folded=True):
    cosines, hard_weights = np.polynomial.legendre.leggauss(5)
    incoming = list(incoming_rule(4, 1e-5, 24.) if part == 'expensive' else compact_rule(128, 1e-5, 24.))
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


def source_components(parameters, difference_model, control_model, rule):
    difference = difference_model.real(parameters, angular=4, radial=18, rule=rule)
    control = control_model.real(parameters, angular=4, radial=18, rule=rule)
    scalar, loop_path = owned_loop(parameters)
    weak.vacuum.mp.mp.dps = 60
    vacuum = float(weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
        + weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
    jump, product = difference_model.born_data(parameters)
    values = dict(difference=difference['total'], control=control['total'],
        virtual=.5 * (vacuum + scalar) * product, state=difference_model.state_correction(parameters)['total'])
    return values, scalar, loop_path, max(difference['event_energy_null'], control['event_energy_null'])
